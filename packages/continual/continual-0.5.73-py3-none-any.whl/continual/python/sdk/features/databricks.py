import os
import base64
from datetime import datetime
import json
from textwrap import dedent
import time
import tempfile
import logging
import random
from pprint import pformat
from typing import List
from jinja2 import Template
import uuid
import requests
import traceback
from pathlib import Path
from functools import wraps
import sqlalchemy as db
from sqlalchemy.exc import (
    IntegrityError,
    NoSuchTableError,
    ProgrammingError,
    OperationalError,
)
from databricks_api import DatabricksAPI
from sqlalchemy.sql.schema import MetaData

from continual.services.dataingest.gcs_source import FeatureSourceCloudStore

from .featurestore import FeatureStore, Typemap
from .prediction_store import PredictionStore, chunk_it

import pandas as pd

from continual.python.sdk.exceptions import InvalidArgumentError
from continual.python.utils.utils import (
    should_enable_databricks_registration,
)

from continual.rpc.management.v1 import management_types_pb2, types

from .query_templates import stats_template_databricks

from .dialects import DatabricksDialect  # don't remove

logging.getLogger("pyhive").setLevel(logging.WARNING)
logging.getLogger("databricks.sql.client").setLevel(logging.WARNING)


def handle_databricks_exception(func):
    """Decorator that parses Databricks exceptions raised through SQLAlchemy.

    Args:
        func: Function to wrap.
    Returns:
        A function that will raise an informative exception.
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if "databricks.sql.exc.OperationalError" in str(e):
                error_str = str(e)
                for line in error_str.splitlines():
                    if (
                        line.startswith("Error message:")
                        and "org.apache.spark.SparkDriverExecutionException:"
                        not in line
                    ):
                        raise InvalidArgumentError(message=line, details=None)
                for line in error_str.splitlines():
                    if (
                        line.startswith("Caused by:")
                        and "org.apache.spark.SparkDriverExecutionException" not in line
                    ):
                        raise InvalidArgumentError(message=line, details=None)
                raise
        except:
            raise

    return wrapped_func


WORKSPACE_DIR = "/FileStore/Continual"
SUPPORTED_RUNTIMES = set(["10.5.x-cpu-ml-scala2.12"])
SYNC_JOB_TASK_KEY = "sync"

CONTINUAL_USER_AGENT = "Continual/1.0"


class DatabricksFeatureStore(FeatureStore, PredictionStore):

    DATABRICKS_TYPEMAP = {
        "object": "STRING",
        "int64": "INT",
        "bool": "BOOLEAN",
        "float64": "FLOAT",
        "datetime64": "TIMESTAMP",
        "datetime64[ns]": "TIMESTAMP",
        "timedelta": "STRING",
        "timedelta[ns]": "STRING",
        "category": "STRING",
        "FIXED": "FLOAT",
        "REAL": "FLOAT",
        "FLOAT": "FLOAT",
        "TEXT": "STRING",
        "DATE": "DATE",
        "TIMESTAMP": "TIMESTAMP",
        "VARIANT": "STRING",
        "OBJECT": "STRING",
        "ARRAY": "ARRAY<STRING>",
        "BINARY": "BINARY",
        "TIME": "TIMESTAMP",
        "BOOL": "BOOLEAN",
        "NUMBER": "FLOAT",
        "FLOAT64": "FLOAT",
        "INTEGER": "INT",
        "INT64": "INT",
        "SMALLINT": "INT",
        "TINYINT": "INT",
        "BIGINT": "INT",
        "NUMERIC": "FLOAT",
        "DECIMAL": "FLOAT",
        "BIGNUMERIC": "FLOAT",
        "BIGDECIMAL": "FLOAT",
    }

    def __init__(
        self,
        data_store,
        source,
        cfg,
        environment: management_types_pb2.Environment = None,
        revive_cluster=False,
    ):
        self.data_store = data_store
        config = data_store.databricks
        db_url = "databricks+connector://token:{}@{}:{}/default".format(
            config.token, config.host, config.port
        )
        self.is_gcp = ".gcp." in config.host
        self.is_azure = "adb-" in config.host or "azuredatabricks" in config.host
        self.is_aws = not self.is_gcp and not self.is_azure

        self.enable_registration = should_enable_databricks_registration(
            self.data_store
        )

        if revive_cluster:
            self._revive_cluster()

        self.engine = db.create_engine(
            db_url,
            connect_args={
                "http_path": config.http_path,
                "user-agent": CONTINUAL_USER_AGENT,
            },
        )
        self.connection = self.engine.connect()
        self.trans = None
        self.environment = environment

        self.api = DatabricksAPI(host=config.host, token=config.token)

        super(DatabricksFeatureStore, self).__init__()

    def set_db_schema(self, db_schema):
        self.db_schema = db_schema

    @handle_databricks_exception
    def cleanup(self):
        self.connection.execute(
            "DROP DATABASE IF EXISTS {} CASCADE".format(self.db_schema)
        )
        return

    @handle_databricks_exception
    def close(self):
        self.connection.close()

    @handle_databricks_exception
    def create_project_schema(self):
        if self.db_schema == None:
            raise InvalidArgumentError("schema_name is required")
        # try to see if the schema exists first
        try:
            print(f"Attempting to create project schema: {self.db_schema}")
            temp_id = random.randint(0, 10000)
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS {}.test_permissions_{} (id INTEGER)".format(
                    self.db_schema, temp_id
                )
            )
            self.connection.execute(
                "DROP TABLE IF EXISTS {}.test_permissions_{}".format(
                    self.db_schema, temp_id
                )
            )
        except Exception:
            logging.debug("database does not appear to exist - create")
            self.connection.execute(
                "CREATE DATABASE IF NOT EXISTS {}".format(self.db_schema)
            )
            logging.debug("database created successfully.")

    @handle_databricks_exception
    def create_featureset_view(self, feature_set: management_types_pb2.FeatureSet):
        project, table_name = self.get_table_name(feature_set)
        table_name = "featureset_{}".format(table_name)
        query = feature_set.schema.query.strip().rstrip(";")
        view_name = "{}.{}".format(self.db_schema, table_name)
        # self.connection.execute(
        #     "CREATE OR REPLACE VIEW {} AS ({})".format(
        #         view_name, query
        #     )
        # )

        feature_table_url = "/2.0/feature-store/feature-tables/get?name={}".format(
            view_name
        )

        sync_action = "create"
        res = self._rest_api_call(feature_table_url, method="GET")
        logging.info(f"feature table GET: {res}")
        if res.get("error_code") != "RESOURCE_DOES_NOT_EXIST":
            sync_action = "update"

        logging.info("feature_set: {}".format(feature_set))
        schema = types.FeatureSetSchema.from_proto(feature_set.schema).to_dict()
        dbfs_schema_path = self._upload_schema(schema)

        start = time.time()
        logging.info(
            "create_featureset_view kicking off sync job for creating databricks feature table ..."
        )

        try:
            self._run_databricks_sync(
                [sync_action, "/dbfs" + dbfs_schema_path, "--table", view_name]
            )
            res = self._rest_api_call(
                "/2.0/feature-store/feature-tables/update",
                method="PATCH",
                body={
                    "name": view_name,
                    "description": "\n".join(
                        [
                            "# ![](https://assets.website-files.com/608c6fda09a6be56ba6844df/608c6fda09a6befa68684532_Symbol.svg)&nbsp;&nbsp;&nbsp;&nbsp;Declaratively Managed by Continual.ai ",
                            "## Description",
                            feature_set.schema.description
                            or "_{}_".format("No description provided."),
                            "## Documentation",
                            feature_set.schema.documentation
                            or "_{}_".format("No documentation provided."),
                            "## Links",
                            "Feature Set: {}".format(
                                "https://cloud.continual.ai/" + feature_set.name
                            ),
                            "Edit Feature Set: {}".format(
                                "https://cloud.continual.ai/"
                                + feature_set.name
                                + "/edit"
                            ),
                            "## Current YAML",
                            "```yaml",
                            feature_set.schema_text,
                            "```",
                        ]
                    ),
                },
            )
            logging.info("update call to feature set: {}".format(res))
        except Exception as e:
            logging.info(
                "create_featureset_view sync job took {} seconds".format(
                    time.time() - start
                )
            )
            raise e
        finally:
            self._delete_file(dbfs_schema_path)

    @handle_databricks_exception
    def create_feature_table(self, feature_set):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.
        Returns None
        """
        if feature_set.schema.query is not None and feature_set.schema.query != "":
            if self.enable_registration:
                self.create_featureset_view(feature_set)
            else:
                super().create_featureset_view(feature_set)
            return

        _, table_name = self.get_table_name(feature_set)
        table_name = "featureset_{}".format(table_name)
        meta = db.MetaData(schema=self.db_schema)

        self.create_project_schema()

        columns = []

        for f in feature_set.schema.columns:
            columns.append(db.Column(f.name, Typemap[f.type]))

        db.Table(table_name, meta, *columns)

        # Following retry logic is added in case a parallel operation
        # creates a schema that might not have existed at the start of the session.
        count = 0
        done = False
        while not done:
            try:
                meta.create_all(self.engine)
                done = True
            except (IntegrityError, ProgrammingError):
                logging.debug("Error while creating feature table " + str(count))
                count = count + 1
                if count == 2:
                    done = True

        self.connection.execute(
            "CONVERT TO DELTA {}.{} NO STATISTICS".format(self.db_schema, table_name)
        )

        if not self.enable_registration:
            return

        table_name = "{}.{}".format(self.db_schema, table_name)

        feature_table_url = "/2.0/feature-store/feature-tables/get?name={}".format(
            table_name
        )

        sync_action = "create"
        res = self._rest_api_call(feature_table_url, method="GET")
        if res.get("error_code") != "RESOURCE_DOES_NOT_EXIST":
            sync_action = "update"

        schema = types.FeatureSetSchema.from_proto(feature_set.schema).to_dict()
        dbfs_schema_path = self._upload_schema(schema)

        start = time.time()
        logging.info(
            "create_feature_table kicking off sync job for creating databricks feature table ..."
        )

        try:
            self._run_databricks_sync(
                [sync_action, "/dbfs" + dbfs_schema_path, "--table", table_name]
            )
        except Exception as e:
            logging.info(
                "create_feature_table sync job took {} seconds".format(
                    time.time() - start
                )
            )
            raise e
        finally:
            self._delete_file(dbfs_schema_path)

    @handle_databricks_exception
    def delete_project_schema(self, schema_name):
        self.connection.execute(
            "DROP DATABASE IF EXISTS {} CASCADE".format(schema_name)
        )

    @handle_databricks_exception
    def drop_featureset_view(self, name):
        if not self.enable_registration:
            return super().drop_featureset_view(name)

        project, table_name = self.get_data_table_name(name)
        # self.connection.execute(
        #     "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, table_name)
        # )

        feature_table_name = "{}.{}".format(self.db_schema, table_name)
        feature_table_url = "/2.0/feature-store/feature-tables/get?name={}".format(
            feature_table_name
        )
        res = self._rest_api_call(feature_table_url, method="GET")
        if res.get("error_code") != "RESOURCE_DOES_NOT_EXIST":
            start = time.time()
            logging.info(
                "create_feature_table kicking off sync job for creating databricks feature table ..."
            )

            try:
                self._run_databricks_sync(["delete", feature_table_name])
            except Exception as e:
                logging.info(
                    "create_feature_table sync job took {} seconds".format(
                        time.time() - start
                    )
                )
                raise e
            finally:
                try:
                    self.connection.execute(
                        "DROP TABLE IF EXISTS {}".format(feature_table_name)
                    )
                except Exception as e:
                    logging.error(e)
        else:
            try:
                self.connection.execute(
                    "DROP VIEW IF EXISTS {}".format(feature_table_name)
                )
            except Exception as e:
                logging.error(e)

        return

    def get_type(self) -> str:
        return "databricks"

    def is_hosted(self):
        return False

    @handle_databricks_exception
    def get_database_names(self):
        databases = []
        result_proxy = self.connection.execute("SHOW DATABASES")
        for rowproxy in result_proxy:
            d = {}
            for col, value in rowproxy.items():
                d[col] = value
            databases.append(d["databaseName"])
        return databases

    def get_table_names(self, database, schema):
        tables = []
        result_proxy = self.connection.execute("SHOW TABLES FROM {}".format(database))
        for rowproxy in result_proxy:
            d = {}
            for col, value in rowproxy.items():
                d[col] = value
            tables.append(d["tableName"])
        return tables

    @handle_databricks_exception
    def get_column_names(self, database, schema, table):
        columns = []
        type_map = {}

        result_proxy = self.connection.execute(
            "DESCRIBE TABLE {}.{}".format(database, table)
        )
        for rowproxy in result_proxy:
            d = {}
            for col, value in rowproxy.items():
                d[col] = value

            columns.append(d["col_name"])
            if d["data_type"]:
                type_map[d["col_name"]] = d["data_type"]

        return columns, type_map

    @handle_databricks_exception
    def get_schema_names(self, database):
        # Databricks does not have Schemas, this is equivalent to SHOW DATABASES
        return self.get_database_names()

    @handle_databricks_exception
    def get_stats_query_template(self):
        return stats_template_databricks

    @handle_databricks_exception
    def get_prediction_table(self, model):
        project_id, pred_table = self.get_model_prediction_table_name(model)
        print("Prediction table in " + self.db_schema)
        try:
            tab = db.Table(
                pred_table,
                db.MetaData(schema=self.db_schema),
                autoload=True,
                autoload_with=self.engine,
            )
            return tab
        except NoSuchTableError:
            # Todo perhaps not capture the error here.
            return None

    @handle_databricks_exception
    def _get_existing_ml_clusters(self) -> List[str]:
        cluster_ids = []
        resp = self._rest_api_call("/2.0/clusters/list", method="GET")

        if "clusters" in resp:
            logging.info(
                f"_get_existing_ml_clusters - all clusters: {resp.get('clusters')}"
            )
            for cluster in resp["clusters"]:
                if (
                    cluster.get("state", "") == "RUNNING"
                    and cluster.get("spark_version", "") in SUPPORTED_RUNTIMES
                    and cluster.get("cluster_id")
                ):
                    cluster_ids.append(cluster["cluster_id"])

        return cluster_ids

    @handle_databricks_exception
    def _get_all_clusters(self) -> List[dict]:
        clusters = []
        resp = self._rest_api_call("/2.0/clusters/list", method="GET")

        if "clusters" in resp:
            for cluster in resp["clusters"]:
                if cluster.get("cluster_id"):
                    clusters.append(cluster)

        return clusters

    @handle_databricks_exception
    def _revive_cluster(self):
        clusters = self._get_all_clusters()
        if any(
            map(
                lambda c: c.get("state") == "RUNNING"
                and c.get("cluster_id") in self.data_store.databricks.http_path,
                clusters or list(),
            )
        ):
            logging.debug("Existing cluster detected. Exiting _revive_cluster ...")
        elif len(clusters) > 0:
            cluster_to_start = clusters[0]
            cluster_id = cluster_to_start["cluster_id"]

            resp = self._rest_api_call(
                "/2.0/clusters/start", body={"cluster_id": cluster_id}, method="POST"
            )

            resp = self._rest_api_call(
                "/2.0/clusters/get", body={"cluster_id": cluster_id}
            )
            logging.info("Waiting for cluster to start ...")
            while resp.get("state") != "RUNNING":
                time.sleep(5)
                resp = self._rest_api_call(
                    "/2.0/clusters/get", body={"cluster_id": cluster_id}
                )
                print(resp.get("state"))

            logging.debug("Successfully revived cluster.")

    @property
    def single_node_cluster_config(self) -> dict:
        if self.is_gcp:
            return dict()  # unsupported

        node_type = "m4.large"  # aws
        if self.is_azure:
            node_type = "Standard_DS3_v2"

        config = {
            "spark_version": "10.5.x-cpu-ml-scala2.12",
            "node_type_id": node_type,
            "driver_node_type_id": node_type,
            "num_workers": 0,
            "spark_conf": {
                "spark.databricks.cluster.profile": "singleNode",
                "spark.master": "local[*]",
            },
            "custom_tags": {"ResourceClass": "SingleNode"},
        }

        if self.is_aws:
            config.update(
                {
                    "enable_elastic_disk": True,
                    "aws_attributes": {"availability": "ON_DEMAND"},
                }
            )

        return config

    @handle_databricks_exception
    def _run_databricks_sync(self, args: list) -> dict:
        if not args:
            raise ValueError("Cannot run Databricks sync job without arguments")

        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "databricks_sync.jinja2"
        )

        sync_executable_path = ""

        try:
            with tempfile.NamedTemporaryFile() as temp:
                with open(template_path) as template_file:
                    template = Template(template_file.read())

                    with open(temp.name, "w") as f:
                        f.write(template.render(is_gcp=True, args=args))

                    sync_executable_path = self._upload_file(
                        temp.name,
                        dest_path="{}/{}/{}_sync.py".format(
                            WORKSPACE_DIR, self.db_schema, random.randint(0, 10_000_000)
                        ),
                    )

            sync_task = {
                "task_key": SYNC_JOB_TASK_KEY,
                "description": "Syncing metadata from Continual into Databricks.",
                "new_cluster": self.single_node_cluster_config,
                # "notebook_task": {
                #     "notebook_path": sync_executable_path,
                # }
                "spark_python_task": {
                    "python_file": "dbfs:" + sync_executable_path,
                    "parameters": args,
                },
            }

            existing_cluster_ids = self._get_existing_ml_clusters()
            if existing_cluster_ids:
                existing_cluster_id = random.choice(existing_cluster_ids)
                logging.info(
                    "randomly selected cluster w/ ID ({}) for Databricks sync job.".format(
                        existing_cluster_id
                    )
                )
                sync_task["existing_cluster_id"] = existing_cluster_id
                del sync_task["new_cluster"]
            else:
                logging.info(
                    "no existing cluster found with a supported runtime. dynamically creating ..."
                )

            res = self._rest_api_call(
                "/2.1/jobs/runs/submit",
                body={
                    "run_name": "Continual.ai Sync",
                    "idempotency_key": SYNC_JOB_TASK_KEY,
                    "tasks": [sync_task],
                },
            )

            if not res or (res and res.get("error_code") or not res.get("run_id")):
                logging.error("error while submitting one-off job run: {}".format(res))
                raise ValueError(
                    "Encountered an error while attempting to run sync job."
                )

            run_id = res["run_id"]
            res = self._rest_api_call(
                "/2.1/jobs/runs/get?run_id={}".format(run_id), method="GET"
            )

            task_id = None

            if len(res.get("tasks", [])) > 0:
                tasks = res["tasks"]
                if "run_id" in tasks[0] and tasks[0]:
                    task_id = tasks[0]["run_id"]

            if task_id is None:
                raise ValueError("Could not find task ID for sync job execution.")

            start = time.time()
            task_state = "PENDING"
            while task_state not in [
                "SUCCESS",
                "SUCCEEDED",
                "FAILED",
                "TERMINATED",
                "CANCELED",
                "CANCELLED",
            ]:
                res = self._rest_api_call(
                    "/2.1/jobs/runs/get-output?run_id={}".format(task_id), method="GET"
                )
                task_state = self._parse_sync_task_state(res)
                logging.info("Sync job output: {}".format(pformat(res)))
                logging.info("Sync task state: {}".format(task_state))
                logging.info(
                    "Elapsed time so far: {} seconds ...".format(time.time() - start)
                )
                time.sleep(10)

            logging.info("Final sync job output: {}".format(pformat(res)))
            logging.info(
                "Databricks sync task returned state ({}) in {} seconds ...".format(
                    task_state, time.time() - start
                )
            )

            if task_state == "SUCCESS" or task_state == "SUCCEEDED":
                return

            error = res.get("error", "Failed to complete sync job.")
            raise ValueError(error)
        except:
            raise
        finally:
            if sync_executable_path:
                self._delete_file(sync_executable_path)

    def _parse_sync_task_state(self, output: dict) -> str:
        metadata = output.get("metadata", {}) or dict()
        tasks = metadata.get("tasks", []) or []
        for task in tasks:
            if task.get("task_key") == SYNC_JOB_TASK_KEY:
                return task.get("state", {}).get("result_state", "PENDING")
        return "PENDING"

    @handle_databricks_exception
    def _rest_api_call(
        self,
        resource: str,
        body: dict = {},
        method: str = "POST",
        headers: dict = {},
        files: dict = {},
    ) -> dict:
        api_url = "https://{}/api/".format(self.data_store.databricks.host)
        if resource.startswith("/"):
            resource = resource[1:]
        api_url += resource
        headers.update(
            {
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            }
        )
        if method == "GET":
            response = requests.get(api_url, headers=headers, json=body)
        elif method == "PATCH":
            response = requests.patch(api_url, headers=headers, json=body)
        else:
            response = requests.post(api_url, headers=headers, json=body, files=files)
        return response.json()

    @handle_databricks_exception
    def _dbfs_rpc(self, action: str, body: dict) -> dict:
        """
        A helper function to make the DBFS API request, request/response is encoded/decoded as JSON.
        Credit: https://docs.databricks.com/dev-tools/api/latest/examples.html#dbfs-large-files
        """
        response = requests.post(
            "https://{}/api/2.0/dbfs/{}".format(
                self.data_store.databricks.host, action
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            json=body,
        )
        return response.json()

    @handle_databricks_exception
    def _delete_file(self, file_path: str) -> bool:
        try:
            self._dbfs_rpc("delete", {"path": file_path})
            return True
        except:
            return False

    @handle_databricks_exception
    def _dbfs_rpc_get(self, action: str, params: dict) -> dict:
        """
        A helper function to make the DBFS API request, request/response is encoded/decoded as JSON.
        Credit: https://docs.databricks.com/dev-tools/api/latest/examples.html#dbfs-large-files
        """
        response = requests.get(
            "https://{}/api/2.0/dbfs/{}".format(
                self.data_store.databricks.host, action
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            params=params,
        )
        return response.json()

    @handle_databricks_exception
    def create_model(self, model):
        response = requests.post(
            "https://{}/api/2.0/preview/mlflow/registered-models/create".format(
                self.data_store.databricks.host
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            json={"name": model.schema.name},
        )

        response = requests.patch(
            "https://{}/api/2.0/preview/mlflow/registered-models/update".format(
                self.data_store.databricks.host
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            json={
                "name": model.schema.name,
                "description": dedent(
                    """
                # ![](https://assets.website-files.com/608c6fda09a6be56ba6844df/608c6fda09a6befa68684532_Symbol.svg)&nbsp;&nbsp;&nbsp;&nbsp;Declaratively Managed by Continual.ai 

                ## Description

                {description}

                ## Documentation

                {documentation}

                ## Links

                Model: {model_link}
                Edit Model: {edit_model_link}

                ## Current YAML

                ```yaml
                {model_yaml}
                ```
                """
                ).format(
                    description=model.schema.description
                    or "_{}_".format("No description provided."),
                    documentation=model.schema.documentation
                    or "_{}_".format("No documentation provided."),
                    model_link="https://cloud.continual.ai/{}".format(model.name),
                    edit_model_link="https://cloud.continual.ai/{}/edit".format(
                        model.name
                    ),
                    model_yaml=model.schema_text,
                ),
            },
        )
        return response.json()

    @handle_databricks_exception
    def create_model_version(self, model, source, version_id):
        response = requests.post(
            "https://{}/api/2.0/preview/mlflow/model-versions/create".format(
                self.data_store.databricks.host
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            json={"name": model.schema.name, "source": source},
        )

        model_version = response.json() or dict()

        logging.info(f"created databricks model version: {model_version}")

        update_description_body = {
            "name": model.schema.name,
            "description": dedent(
                """
            # ![](https://assets.website-files.com/608c6fda09a6be56ba6844df/608c6fda09a6befa68684532_Symbol.svg)&nbsp;&nbsp;&nbsp;&nbsp;Declaratively Managed by Continual.ai 

            ## Description

            {description}

            ## Documentation

            {documentation}

            ## Links

            Model: {model_link}
            Edit Model: {edit_model_link}
            Model Version: {model_version_link}

            ## Current YAML

            ```yaml
            {model_yaml}
            ```
            """
            ).format(
                description=model.schema.description
                or "_{}_".format("No description provided."),
                documentation=model.schema.documentation
                or "_{}_".format("No documentation provided."),
                model_link="https://cloud.continual.ai/{}".format(model.name),
                edit_model_link="https://cloud.continual.ai/{}/edit".format(model.name),
                model_version_link="https://cloud.continual.ai/{}/versions/{}".format(
                    model.name, version_id
                ),
                model_yaml=model.schema_text,
            ),
        }

        if model_version.get("model_version", dict()).get("version"):
            model_version_payload = update_description_body
            model_version_payload["version"] = model_version["model_version"]["version"]
            response = requests.patch(
                "https://{}/api/2.0/preview/mlflow/model-versions/update".format(
                    self.data_store.databricks.host
                ),
                headers={
                    "Authorization": "Bearer {}".format(
                        self.data_store.databricks.token
                    ),
                    "User-Agent": CONTINUAL_USER_AGENT,
                },
                json=model_version_payload,
            )

        logging.info(f"update model version description response: {response}")

        response = requests.patch(
            "https://{}/api/2.0/preview/mlflow/registered-models/update".format(
                self.data_store.databricks.host
            ),
            headers={
                "Authorization": "Bearer {}".format(self.data_store.databricks.token),
                "User-Agent": CONTINUAL_USER_AGENT,
            },
            json=update_description_body,
        )
        return response.json()

    @handle_databricks_exception
    def upload_directory(self, dir_path: str, dest_dir_path: str) -> str:
        files = list(Path(dir_path).rglob("*"))
        # dest_base = "dbfs:/FileStore/continual_"
        logging.info("upload {} files".format(len(files)))
        for file in files:
            file_str = str(file)
            if os.path.isfile(file_str):
                dest_path = f"{dest_dir_path}{file_str[len(dir_path):]}"
                logging.info("upload {} to {}".format(file_str, dest_path))
                self.upload_file(file_str, dest_path)

    @handle_databricks_exception
    def upload_file(self, file_path: str, dest_path: str) -> str:
        handle = self._dbfs_rpc("create", {"path": dest_path, "overwrite": "true"})
        if "handle" in handle:
            handle = handle["handle"]
        elif (
            "error_code" in handle
            and handle["error_code"].upper() == "FEATURE_DISABLED"
        ):
            raise ValueError(
                "The DBFS API is disabled for this Databricks installation, and cannot be used to upload files."
            )

        with open(file_path, "rb") as f:
            while True:
                # A block can be at most 1MB
                contents = f.read(2 ** 20)
                if len(contents) == 0:
                    break
                data = base64.b64encode(contents).decode()
                self._dbfs_rpc("add-block", {"handle": handle, "data": data})
        # close the handle to finish uploading
        self._dbfs_rpc("close", {"handle": handle})

        return dest_path

    @handle_databricks_exception
    def _upload_schema(self, schema: dict) -> str:
        if not schema.get("name") or not schema.get("type"):
            raise ValueError("cannot upload a schema without a type and a name")

        path_component = "models" if schema["type"] == "model" else "featureSets"

        # /FileStore/Continual/my_project/featureSets/
        # or
        # /FileStore/Continual/my_project/models
        schema_path = "{}/{}/{}".format(WORKSPACE_DIR, self.db_schema, path_component)

        res = self._rest_api_call("/2.0/workspace/mkdirs", body={"path": schema_path})
        if res.get("error_code"):
            raise ValueError("Exception while uploading schema: {}".format(res))

        encoded_schema = json.dumps(schema, separators=(",", ":"))

        uploaded_path = ""
        with tempfile.NamedTemporaryFile() as temp:
            with open(temp.name, "w") as f:
                f.write(encoded_schema)
            uploaded_path = self._upload_file(
                temp.name, dest_path="{}/{}.json".format(schema_path, schema["name"])
            )

        return uploaded_path

    @handle_databricks_exception
    def _upload_file(self, file_path: str, dest_path: str = "", **kwargs) -> str:
        if not dest_path:
            dest_path = "/tmp_continual_file__{}".format(random.randint(1, 10_000))

        handle = self._dbfs_rpc("create", {"path": dest_path, "overwrite": "true"})
        if "handle" in handle:
            handle = handle["handle"]
        elif (
            "error_code" in handle
            and handle["error_code"].upper() == "FEATURE_DISABLED"
        ):
            raise ValueError(
                "The DBFS API is disabled for this Databricks installation, and cannot be used to upload files."
            )

        with open(file_path, "rb") as f:
            while True:
                # A block can be at most 1MB
                contents = f.read(2 ** 20)
                if len(contents) == 0:
                    break
                data = base64.b64encode(contents).decode()
                self._dbfs_rpc("add-block", {"handle": handle, "data": data})
        # close the handle to finish uploading
        self._dbfs_rpc("close", {"handle": handle})

        return dest_path

    @handle_databricks_exception
    def _upload_file_via_import(
        self, file_path: str, dest_path: str, language: str = "PYTHON"
    ) -> str:
        """
        WARNING: this does not work yet.
        """
        res = self._rest_api_call(
            "/2.0/workspace/mkdirs", body={"path": os.path.dirname(dest_path)}
        )

        if res and res.get("error_code"):
            raise ValueError(json.dumps(res))

        contents = ""
        with open(file_path, "rb") as f:
            contents = f.read()

        res = self._rest_api_call(
            "/2.0/workspace/import",
            body={
                "path": dest_path,
                "content": base64.b64encode(contents).decode(),
                "language": "PYTHON",
                "overwrite": "true",
            },
        )

        if res and res.get("error_code"):
            raise ValueError(json.dumps(res))

        return dest_path

    @handle_databricks_exception
    def write_prediction(
        self,
        df: pd.DataFrame,
        id_column_name: str,
        ts_column_name: str,
        model_query: any,
        output_name: str,
        job_name: str,
        job_start_time: datetime,
        model,
        model_version,
        time_index_dtype,
    ):
        logging.info(
            "in write_prediction for [{}]:[{}]".format(
                job_name, job_start_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        if self.data_store is None:
            logging.debug("skipping write_prediction")
            return

        project_id, pred_table = self.get_model_prediction_table_name(model)
        df = self._process_dataframe(
            df, id_column_name, ts_column_name, job_name, model_version
        )
        df["prediction_time"] = job_start_time.strftime("%Y-%m-%dT%H:%M:%S")

        tab = self.get_prediction_table(model)
        if tab is None:
            print("Prediction table not found")
            logging.debug("Prediction table not found")
            return

        # set chained assignent to warn in case an underlying model has set to raise
        # TODO: determine if there's a better method of mapping the json values
        pd.set_option("mode.chained_assignment", "warn")

        prediction_details_column = f"{output_name}_prediction_details"

        col_names, type_map = self.get_column_names(self.db_schema, "", pred_table)
        existing_col_order = df.columns.tolist()
        sorted_col_names = list(filter(lambda c: c in existing_col_order, col_names))
        df = df[sorted_col_names]

        if prediction_details_column in df.columns:
            df[prediction_details_column] = df[prediction_details_column].map(
                json.dumps
            )

        self._two_stage_insert(df, pred_table, exists="append")

        count_query = f"SELECT COUNT(1) from {self.db_schema}.{pred_table} WHERE batch_prediction = '{job_name}'"
        result = self.connection.execute(count_query)
        for row in result:
            return row[0]
        return 0

    @handle_databricks_exception
    def _two_stage_insert(
        self,
        df: pd.DataFrame,
        table_name: str,
        exists: str = "fail",
    ):
        ch = chunk_it(0, df.shape[0], step=10_000)
        while ch is not None:
            df_slice = df[ch[0] : ch[1]]
            logging.info("writing features to table {}".format(table_name))
            logging.info("feature dtypes: {}".format(df_slice.dtypes))

            try:
                chunk_start = time.time()
                logging.info(
                    "Writing chunk ({} to {}) of DataFrame ...".format(ch[0], ch[1])
                )
                df_slice.to_sql(
                    table_name,
                    self.connection,
                    schema=self.db_schema,
                    if_exists=exists,
                    method="multi",
                    index=False,
                )
                logging.info(
                    "Done. Chunk took {}s to write.".format(time.time() - chunk_start)
                )
                if ch[0] == 0:
                    logging.info("Converting to Delta table ...")
                    delta_start = time.time()
                    self.connection.execute(
                        "CONVERT TO DELTA {}.{} NO STATISTICS".format(
                            self.db_schema, table_name
                        )
                    )
                    logging.info(
                        "Done converting into Delta. Took {}s".format(
                            time.time() - delta_start
                        )
                    )
            except:
                traceback.print_exc()
                logging.debug("write failed to execute - aborting")
                raise
            ch = chunk_it(ch[1], df.shape[0], step=10_000)

    @handle_databricks_exception
    def _create_prediction_model_table(
        self, model, model_pred_name, meta: MetaData, problem_type
    ):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.≈
        Returns None
        """

        index = None
        time_index = None
        target_column = model.schema.target
        target_column_dtype = db.TEXT
        for f in model.schema.columns:
            if (
                f.type == management_types_pb2.FieldType.INDEX
                or f.name == model.schema.index
            ):
                index = f
            elif (
                f.type == management_types_pb2.FieldType.TIME_INDEX
                or f.name == model.schema.time_index
            ):
                time_index = f
            elif f.name == target_column:
                target_column_dtype = Typemap[f.dtype]

        columns = []
        columns.append(db.Column("batch_prediction", db.Text))
        columns.append(db.Column("model_version", db.Text))
        columns.append(db.Column("prediction_time", db.TIMESTAMP()))
        columns.append(db.Column(f"features", db.Text))

        if index is not None:
            columns.append(db.Column(index.name, Typemap[index.dtype]))

        if time_index is not None:
            columns.append(db.Column(time_index.name, Typemap[time_index.dtype]))
        columns.append(db.Column(f"{target_column}_prediction", target_column_dtype))
        if problem_type == "multiclass_classification":
            columns.append(db.Column(f"{target_column}_prediction_details", db.Text))
            columns.append(db.Column(f"{target_column}_prediction_score", db.Float))
        if problem_type == "binary_classification":
            columns.append(
                db.Column(f"{target_column}_true_prediction_score", db.Float)
            )

        table = db.Table(model_pred_name, meta, *columns)
        logging.info("databricks model prediction table: {}".format(table))

        # Following retry logic is added in case a parallel operation
        # creates a schema that might not have existed at the start of the session.
        count = 0
        done = False
        while not done:
            try:
                table.create(self.engine, checkfirst=False)
                # meta.create_all(self.engine, checkfirst=False)
                done = True
            except (IntegrityError, ProgrammingError):
                logging.debug(traceback.format_exc())
                logging.debug("Error while creating model table " + str(count))
                count = count + 1
                if count == 2:
                    raise

        self.connection.execute(
            "CONVERT TO DELTA {}.{} NO STATISTICS".format(
                self.db_schema, model_pred_name
            )
        )

    @handle_databricks_exception
    def load_data(self, filename, table_name, replace=False):
        source = FeatureSourceCloudStore(str(uuid.uuid4()), filename)
        df = source.fetch_all()
        df.columns = [col.lower() for col in df.columns]
        exists = "fail"
        if replace:
            exists = "replace"
        try:
            logging.info(
                "load_data: schema: {}, table_name: {}".format(
                    self.db_schema, table_name.lower()
                )
            )
            self._two_stage_insert(df, table_name.lower(), exists=exists)
        except ValueError:
            traceback.print_exc()

        return table_name.lower()

    @handle_databricks_exception
    def infer_schema(
        self,
        query,
        excludes=None,
        sample_row_count=100,
        allow_invalid_types=False,
        timeout_ms=0,
    ):
        return super().infer_schema(
            query,
            excludes=excludes,
            sample_row_count=sample_row_count,
            allow_invalid_types=allow_invalid_types,
            timeout_ms=timeout_ms,
        )
