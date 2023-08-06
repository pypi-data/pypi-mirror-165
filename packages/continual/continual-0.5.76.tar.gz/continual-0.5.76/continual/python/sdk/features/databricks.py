import os
from datetime import datetime
import json
from textwrap import dedent
import time
import tempfile
import logging
import random
from typing import List
from jinja2 import Template
import uuid
import requests
import traceback
from functools import wraps
import sqlalchemy as db
from sqlalchemy.exc import (
    IntegrityError,
    NoSuchTableError,
    ProgrammingError,
    OperationalError,
)
from sqlalchemy.sql.schema import MetaData
from continual.python.sdk.models import Model

from continual.services.dataingest.gcs_source import FeatureSourceCloudStore

from .featurestore import FeatureStore, Typemap
from .prediction_store import PredictionStore, chunk_it

import pandas as pd

from continual.python.sdk.exceptions import InvalidArgumentError
from continual.python.utils.utils import (
    should_enable_databricks_registration,
)

from continual.rpc.management.v1 import management_types_pb2

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
        cfg: dict = None,
        environment: management_types_pb2.Environment = None,
        revive_cluster=False,
    ):
        self.cfg = cfg or dict()
        logging.info(f"databricks config: {self.cfg}")
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

        start = time.time()
        logging.info(
            "create_featureset_view kicking off sync job for creating databricks feature table ..."
        )

        try:
            self._run_databricks_sync(
                sync_action,
                {"feature_set_name": feature_set.name, "table": view_name},
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

        start = time.time()
        logging.info(
            "create_feature_table kicking off sync job for creating databricks feature table ..."
        )

        try:
            self._run_databricks_sync(
                sync_action,
                {"feature_set_name": feature_set.name, "table": table_name},
            )
        except Exception as e:
            logging.info(
                "create_feature_table sync job took {} seconds".format(
                    time.time() - start
                )
            )
            raise e

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
                self._run_databricks_sync("delete", {"table": feature_table_name})
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
            logging.debug(
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
        node_type = "m4.large"  # aws
        if self.is_azure:
            node_type = "Standard_DS3_v2"
        elif self.is_gcp:
            node_type = "n1-standard-4"

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
            "autotermination_minutes": 10,
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
    def _run_databricks_sync(self, action: str, args: dict) -> dict:
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "databricks_sync.jinja2"
        )

        context_id = ""
        cluster_id = ""
        rendered_template_path = ""

        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                with open(template_path) as template_file:
                    template = Template(template_file.read())

                    api_key = self.cfg.get("authorization", "")
                    endpoint = (
                        self.cfg.get("env_config", dict())
                        .get("Endpoints", dict())
                        .get("management_external", "https://api.continual.ai")
                    )

                    with open(temp.name, "w") as f:
                        f.write(
                            template.render(
                                action=action,
                                api_key=api_key,
                                endpoint=endpoint,
                                args=args,
                            )
                        )
                    with open(temp.name) as f:
                        logging.info(f.read())
                    rendered_template_path = temp.name

            existing_cluster_ids = self._get_existing_ml_clusters()
            if existing_cluster_ids:
                cluster_id = random.choice(existing_cluster_ids)
                logging.info(
                    "randomly selected cluster w/ ID ({}) for Databricks sync job.".format(
                        cluster_id
                    )
                )
            else:
                logging.info(
                    "no existing cluster found with a supported runtime. dynamically creating ..."
                )
                cluster_id = self._create_databricks_cluster()

            self._install_continual_pypi_library(cluster_id)

            res = self._rest_api_call(
                "/1.2/contexts/create", {"clusterId": cluster_id, "language": "python"}
            )
            if res.get("error") or not res.get("id"):
                raise ValueError("could not start execution context")

            context_id = res.get("id")

            command_id = ""
            res = self._rest_api_call(
                "/1.2/commands/execute",
                files={
                    "command": (None, open(rendered_template_path, "rb")),
                    "clusterId": cluster_id,
                    "contextId": context_id,
                    "language": "python",
                },
            )

            if res.get("error") or not res.get("id"):
                raise ValueError("could not execute command")

            command_id = res.get("id")

            start = time.time()
            state = ""
            while state not in ("CANCELLED", "ERROR", "FINISHED"):
                res = self._rest_api_call(
                    "/1.2/commands/status",
                    params={
                        "clusterId": cluster_id,
                        "contextId": context_id,
                        "commandId": command_id,
                    },
                    method="GET",
                )
                if res.get("error"):
                    break
                logging.info(f"Sync res: {res}")
                state = res.get("status", "").upper()

                logging.info(
                    "Elapsed time so far: {} seconds ...".format(time.time() - start)
                )
                time.sleep(10)

            logging.info(f"Final databricks response: {res}")
            logging.info(
                "Databricks sync task returned state ({}) in {} seconds ...".format(
                    state, time.time() - start
                )
            )

            if res.get("error"):
                raise ValueError(res["error"])
            elif res.get("results", dict()).get("resultType", "") == "error":
                results = res.get("results", dict())
                summary = results.get("summary", "No summary reported.")
                cause = results.get("cause", "No cause reported.")
                error = results.get("error", "No error reported.")
                raise ValueError(
                    f"Failed to completed Databricks sync: summary: {summary}, error: {error}, cause: {cause}"
                )
            elif state == "FINISHED":
                return

            raise ValueError("Failed to complete Databricks sync.")

        finally:
            if rendered_template_path and os.path.isfile(rendered_template_path):
                try:
                    os.remove(rendered_template_path)
                except:
                    pass

            if context_id:
                res = self._rest_api_call(
                    "/1.2/contexts/destroy",
                    {"contextId": context_id, "clusterId": cluster_id},
                )

    def _parse_sync_task_state(self, output: dict) -> str:
        metadata = output.get("metadata", {}) or dict()
        tasks = metadata.get("tasks", []) or []
        for task in tasks:
            if task.get("task_key") == SYNC_JOB_TASK_KEY:
                return task.get("state", {}).get("result_state", "PENDING")
        return "PENDING"

    def _create_databricks_cluster(self, config: dict) -> str:
        res = self._rest_api_call("/2.0/clusters/create", config)
        logging.info("start new databricks cluster res: ", res)
        cluster_id = res.get("cluster_id", "")
        if not cluster_id or res.get("error"):
            raise ValueError(res.get("error") or "could not create Databrickc cluster")
        state = ""
        start_time = time.time()
        while state not in (
            "RUNNING",
            "TERMINATING",
            "TERMINATED",
        ):
            res = self._rest_api_call(
                "/2.0/clusters/get", params={"cluster_id": cluster_id}
            )
            state = res.get("state")
            logging.info(f"Waiting on cluster to start. State = {state}")
            time.sleep(5)
        logging.info(f"Finished in {time.time() - start_time} seconds.")
        if state == "RUNNING":
            return cluster_id
        else:
            raise ValueError(res.get("error") or "could not create Databricks cluster")

    def _install_continual_pypi_library(self, cluster_id: str):
        found = False
        res = self._rest_api_call(
            "/2.0/libraries/cluster-status",
            params=dict(cluster_id=cluster_id),
            method="GET",
        )
        logging.info(f"_install_continual_pypi_library uninstall res: {res}")
        library_statuses = res.get("library_statuses", [])
        found = False
        for lib in library_statuses:
            if lib.get("library", {}).get("pypi", {}).get("package", "") == "continual":
                found = True

        if found:
            logging.info("found old version of the continual pypi package")
            res = self._rest_api_call(
                "/2.0/libraries/uninstall",
                {
                    "cluster_id": cluster_id,
                    "libraries": [
                        {"pypi": {"package": "continual==0.5.74"}},
                        {"pypi": {"package": "continual"}},
                    ],
                },
            )
            logging.info(f"uninstalling old continual pypi package res: {res}")

            running = False
            while not running:
                resp = self._rest_api_call(
                    "/2.0/clusters/restart",
                    body={"cluster_id": cluster_id},
                    method="POST",
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
                    logging.info(resp.get("state"))

                logging.debug("Successfully revived cluster.")
                running = True

        logging.info("successfully uninstalled existing continual pypi package")

        res = self._rest_api_call(
            "/2.0/libraries/install",
            {
                "cluster_id": cluster_id,
                "libraries": [{"pypi": {"package": "continual"}}],
            },
        )
        logging.info(f"_install_continual_pypi_library res: {res}")

        state = ""
        start = time.time()
        lib = dict()
        while state not in ("INSTALLED", "SKIPPED", "FAILED", "UNINSTALL_ON_RESTART"):
            elapsed = time.time() - start
            if elapsed >= (60 * 10):
                raise ValueError(
                    "Installing Continual PyPI package on Databricks cluster timed out (>15m)."
                )

            res = self._rest_api_call(
                "/2.0/libraries/cluster-status",
                params=dict(cluster_id=cluster_id),
                method="GET",
            )
            logging.info(f"_install_continual_pypi_library install res: {res}")
            library_statuses = res.get("library_statuses", [])
            for lib in library_statuses:
                if (
                    lib.get("library", {}).get("pypi", {}).get("package", "")
                    == "continual"
                ):
                    state = lib.get("status", "").upper()
            time.sleep(5)

        logging.info(
            f"Completed install wait for Continual PyPI package on Databricks cluster: {res}"
        )
        logging.info(
            f"Final state for Continual PyPI package on Databricks cluster: {state}"
        )

        if state == "INSTALLED":
            return

        raise ValueError(
            " ".join(lib.get("messages", []))
            if lib.get("messages")
            else "Failed to install Continual PyPI package on Databricks cluster."
        )

    @handle_databricks_exception
    def _rest_api_call(
        self,
        resource: str,
        body: dict = {},
        method: str = "POST",
        headers: dict = {},
        files: dict = {},
        params: dict = {},
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
            response = requests.get(api_url, headers=headers, params=params, json=body)
        elif method == "PATCH":
            response = requests.patch(
                api_url, headers=headers, params=params, json=body
            )
        else:
            response = requests.post(
                api_url, headers=headers, params=params, json=body, files=files
            )
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
    def create_model_version(self, model: Model, version_id: str):
        try:
            model_version_name = f"{model.name}/versions/{version_id}"
            self._run_databricks_sync(
                "load_model_artifact", {"model_version_name": model_version_name}
            )
            source = (
                f"dbfs:/FileStore/continual/{model_version_name}/model_{version_id}"
            )
            response = requests.post(
                "https://{}/api/2.0/preview/mlflow/model-versions/create".format(
                    self.data_store.databricks.host
                ),
                headers={
                    "Authorization": "Bearer {}".format(
                        self.data_store.databricks.token
                    ),
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
                    edit_model_link="https://cloud.continual.ai/{}/edit".format(
                        model.name
                    ),
                    model_version_link="https://cloud.continual.ai/{}/versions/{}".format(
                        model.name, version_id
                    ),
                    model_yaml=model.schema_text,
                ),
            }

            if model_version.get("model_version", dict()).get("version"):
                model_version_payload = update_description_body
                model_version_payload["version"] = model_version["model_version"][
                    "version"
                ]
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
                    "Authorization": "Bearer {}".format(
                        self.data_store.databricks.token
                    ),
                    "User-Agent": CONTINUAL_USER_AGENT,
                },
                json=update_description_body,
            )
            return response.json()
        except Exception:
            raise

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
