import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, ProgrammingError

import logging
import traceback
from json import loads, dumps
from google.oauth2 import service_account
from jinja2 import Template
from datetime import datetime
import pandas as pd
import os

from sqlalchemy.sql.schema import MetaData, Table
from continual.python.utils.utils import create_limit_query, is_select_query
from continual.rpc.management.v1 import management_types_pb2
from .prediction_store import PredictionStore
from .featurestore import FeatureStore, Typemap, FilterTables
from continual.python.sdk.exceptions import InvalidArgumentError

# from .query_templates import stats_template_bigquery
from continual.services.dataingest.gcs_source import FeatureSourceCloudStore
import uuid
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

stats_template_bigquery = Template(
    """
 {% for elem in params.AllFeatures %} {% if loop.index > 1 %} UNION ALL {% endif %}
	SELECT {% if elem.Alias %} '{{elem.Alias}}' {% else %} '{{elem.name}}' {% endif %}as `column_name`,
{% if (elem.type == "NUMBER" or elem.type == "REAL" or elem.type == "FIXED") %}
	COALESCE(max(allentities.{{elem.name}}), 0.0) as `max`, COALESCE(min(allentities.{{elem.name}}), 0.0) as `min`,
	COALESCE(avg(allentities.{{elem.name}}), 0.0) as `mean`, COALESCE(stddev(allentities.{{elem.name}}), 0.0) as `sd`,
	0 as `min_length`, 0 as `max_length`, 0 as `distinct_values`, CAST(NULL as timestamp)  as `latest`, CAST(NULL as timestamp)  as `earliest`,
{% elif (elem.type == "TIMESTAMP" or elem.type == "TIMESTAMP_LTZ" or elem.type == "TIMESTAMP_TZ" or elem.type == "TIMESTAMP_NTZ" or elem.type == "DATE") %}
	0.0 as `max`, 0.0 as `min`, 0.0 as `mean`, 0.0 as `sd`, 0 as `min_length`, 0 as `max_length`, 0 as `distinct_values`, 
    cast(max(allentities.{{elem.name}}) as timestamp) as `latest`, cast(min(allentities.{{elem.name}}) as timestamp) as `earliest`,
{% elif (elem.type == "TEXT" or elem.type == "STRING") %}
	0 as `max`, 0 as `min`, 0.0 as `mean`, 0.0 as `sd`, COALESCE(min(length(allentities.{{elem.name}})), 0) as `min_length`,
	COALESCE(max(length(allentities.{{elem.name}})), 0) as `max_length`, COALESCE(count(distinct(allentities.{{elem.name}})), 0) as `distinct_values`,
	CAST(NULL as timestamp)  as `latest`, CAST(NULL as timestamp)  as `earliest`,
{% elif elem.type == "CATEGORICAL" %}
	0 as `max`, 0 as `min`, 0.0 as `mean`, 0.0 as `sd`,
	COALESCE(min(length(allentities.{{elem.name}})), 0) as `min_length`, COALESCE(max(length(allentities.{{elem.name}})), 0) as `max_length`,
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as `distinct_values`, CAST(NULL as timestamp)  as `latest`,
	CAST(NULL as timestamp)  as `earliest`,
{% elif elem.type == "BOOLEAN" %}
	0 as `max`, 0 as `min`, 0.0 as `mean`, 0.0 as `sd`, 0 as `min_length`, 0 as `max_length`,
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as `distinct_values`, CAST(NULL as timestamp)  as `latest`, CAST(NULL as timestamp)  as `earliest`,
{% else %}
	0 as `max`, 0 as `min`, 0.0 as `mean`, 0.0 as `sd`, 0 as `min_length`, 0 as `max_length`, 0 as `distinct_values`,
	CAST(NULL as timestamp)  as `latest`, CAST(NULL as timestamp)  as `earliest`,{% endif %}
	count(*) - count(allentities.{{elem.name}})  as `null_count`,
	count(allentities.{{elem.name}}) as `count`,
	CURRENT_TIMESTAMP as `computed_at`, '{{elem.ctype}}' as `type`
    FROM  {{params.FullName}} as allentities
	{% endfor %}
    """
)


class BigQueryClient:
    def __init__(self, data_store):
        self.data_store = data_store
        if data_store.big_query.auth_file is None:
            return InvalidArgumentError("Invalid GCS credentials file")

        bq_cred = loads(data_store.big_query.auth_file)
        if "project_id" not in bq_cred:
            raise InvalidArgumentError("Invalid GCS credentials file")

        self.client_uuid = str(uuid.uuid4().hex)
        self.project = bq_cred["project_id"]
        logging.info("set bq project to: {}".format(self.project))
        self.cred_file = f"/tmp/{bq_cred['project_id']}_{self.client_uuid}.json"
        with open(self.cred_file, "w") as cred_file:
            cred_file.write(data_store.big_query.auth_file)

        self.credentials = service_account.Credentials.from_service_account_file(
            self.cred_file,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    def __enter__(self):
        try:
            self.client = bigquery.Client(
                project=self.project, credentials=self.credentials
            )
            return self.client, self.project, self.cred_file
        except:
            logging.info(traceback.format_exc())
            raise

    def __exit__(self, type, value, traceback):
        # Exception handling here
        self.client.close()
        if os.path.isfile(self.cred_file):
            os.remove(self.cred_file)


def create_connection(data_store, dataset=None):
    """
    Create bigquery connection given data_store.
    """
    with BigQueryClient(data_store) as (_, project, cred_file):
        logging.info("using bg project for connection: {}".format(project))
        eng = db.create_engine(
            "bigquery://{project}".format(project=project), credentials_path=cred_file
        )

        connection = eng.connect()
        return eng, connection, project


class BigqueryFeatureStore(FeatureStore, PredictionStore):

    """
    BigqueryFeatureStore implements both source of features and featurestore functions.
    Currently sources are not pooled. In a larger tenant with frequent and multiple fetches,
    we would need to consider connection pooling.
    """

    DTYPE_TO_LOGICAL = {
        "FIXED": "NUMBER",
        "FLOAT": "NUMBER",
        "FLOAT64": "NUMBER",
        "INT": "NUMBER",
        "INT64": "NUMBER",
        "SMALLINT": "NUMBER",
        "SMALLINT": "NUMBER",
        "TINYINT": "NUMBER",
        "BYTEINT": "NUMBER",
        "INTEGER": "NUMBER",
        "NUMERIC": "NUMBER",
        "DECIMAL": "NUMBER",
        "BIGNUMERIC": "NUMBER",
        "BIGDECIMAL": "NUMBER",
        "TEXT": "CATEGORICAL",
        "STRING": "CATEGORICAL",
        "DATE": "TIMESTAMP",
        "DATETIME": "TIMESTAMP",
        "TIMESTAMP": "TIMESTAMP",
        "VARIANT": "TEXT",
        "TIMESTAMP_LTZ": "TIMESTAMP",
        "TIMESTAMP_TZ": "TIMESTAMP",
        "TIMESTAMP_NTZ": "TIMESTAMP",
        "OBJECT": "TEXT",
        "ARRAY": "STRING_ARRAY",
        "BYTES": "TEXT",
        "TIME": "TIMESTAMP",
        "BOOLEAN": "BOOLEAN",
        "BOOL": "BOOLEAN",
    }

    def __init__(self, data_store, source=None, cfg=None):
        self.data_store = data_store
        self.source = source
        self.corpus_id = None
        self.client = None

        try:
            self.engine, self.connection, self.bq_project = create_connection(
                data_store
            )
        except Exception:
            raise InvalidArgumentError(
                "Connection to bigquery failed, please check connection settings.",
                details=None,
            )
        super(BigqueryFeatureStore, self).__init__()

    def cleanup(self):
        with BigQueryClient(self.data_store) as (client, _, _):
            dataset_id = "{}.{}".format(client.project, self.db_schema)
            client.delete_dataset(
                dataset_id, delete_contents=True, not_found_ok=True
            )  # Make an API request.
            return

    def close(self):
        self.connection.close()

    def get_type(self) -> str:
        return "bigquery"

    def is_hosted(self):
        return False

    def get_stats_query_template(self):
        return stats_template_bigquery

    def create_prediction_model_table(
        self, model, problem_type, prev_index, prev_time_index
    ):
        """
        Create or update the table used to store predictions.

        This checks to see if the prediction table for this model exists, if it doesn't it creates it. If it does, it updates it if necessary.

        Parameters
        ----------
        model : continual.rpc.management.v1.Model
            The Model definition.
        problem_type : string
            The type of problem the model is solving.  E.g. regression, multiclass_classification, binary_classification.
        prev_index: string
            If there already is a model schema defined, the value of the previous model schema definition's index. Empty string if there is no previous model definition.
        prev_time_index: string
            If there already is a model schema defined, the value of the previous model schema definition's time index. Empty string if there is no previous model definition.
        """
        meta = db.MetaData()

        meta.reflect(bind=self.engine, only=FilterTables(schema=self.db_schema))
        _, model_pred_name = self.get_model_prediction_table_name(model)
        model_table = None
        for t in meta.sorted_tables:
            if f"{self.db_schema}.{model_pred_name}" == t.name:
                model_table = t
        if model_table is None:
            self._create_prediction_model_table(
                model, model_pred_name, meta, problem_type
            )
        else:
            self._update_prediction_model_table(
                model, model_table, problem_type, prev_index, prev_time_index
            )

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
                # a regression prediction is always a floating point number
                if problem_type == "regression":
                    target_column_dtype = db.FLOAT

        columns = []
        columns.append(db.Column("batch_prediction", db.Text))
        columns.append(db.Column("model_version", db.Text))
        columns.append(db.Column("prediction_time", db.TIMESTAMP(timezone=True)))
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

        db.Table(model_pred_name, meta, *columns, schema=self.db_schema)

        # Following retry logic is added in case a parallel operation
        # creates a schema that might not have existed at the start of the session.
        count = 0
        done = False
        while not done:
            try:
                meta.create_all(self.engine)
                done = True
            except (IntegrityError, ProgrammingError):
                logging.debug(traceback.format_exc())
                logging.debug("Error while creating feature table " + str(count))
                count = count + 1
                if count == 2:
                    raise

    def _update_prediction_model_table(
        self, model, model_table: Table, problem_type, prev_index, prev_time_index
    ):

        logging.info(f"update table: {model_table.name}")
        index_column = model.schema.index
        time_index_column = model.schema.time_index
        target_column = model.schema.target
        prediction_col = f"{target_column}_prediction"
        prediction_details_col = f"{target_column}_prediction_details"
        prediction_score_col = f"{target_column}_prediction_score"
        if problem_type == "binary_classification":
            prediction_score_col = f"{target_column}_true_prediction_score"

        if (
            prediction_col in model_table.columns.keys()
            and (index_column == "" or index_column in model_table.columns.keys())
            and (
                time_index_column == ""
                or time_index_column in model_table.columns.keys()
            )
        ):
            # no changes to make
            logging.info("no changes to make to table")
            return
        # rename columns
        old_prediction_col = ""
        old_prediction_details_col = ""
        old_prediction_score_col = ""
        for col_name in model_table.columns.keys():
            if col_name.endswith("_prediction"):
                old_prediction_col = col_name
            if col_name.endswith("_prediction_details"):
                old_prediction_details_col = col_name
            if col_name.endswith("_prediction_score"):
                old_prediction_score_col = col_name

        if old_prediction_col == "":
            raise ValueError(
                f"predictions columms not found in table {model_table.name}"
            )

        indexes_except = ""
        indexes_as = ""

        if index_column != "" and index_column != prev_index:
            indexes_except = f", {prev_index}"
            indexes_as = f", {prev_index} as {index_column}"
        if time_index_column != "" and time_index_column != prev_time_index:
            indexes_except = f"{indexes_except}, {prev_index}"
            indexes_as = f"{indexes_as}, {prev_index} as {index_column}"

        # TODO: fix so we do time index and or index as appropriate
        with BigQueryClient(self.data_store) as (bqc, _, _):
            if problem_type == "multiclass_classification":
                alter_query = f""" CREATE OR REPLACE TABLE `{model_table.name}`  AS
                        SELECT * EXCEPT({old_prediction_col}, {old_prediction_details_col}, {old_prediction_score_col} {indexes_except}) {indexes_as}, {old_prediction_col} as {prediction_col}, 
                        {old_prediction_details_col} as {prediction_details_col}, {old_prediction_score_col} as {prediction_score_col} 
                        FROM `{model_table.name}`"""
                query_job = bqc.query(alter_query)
                query_job.result()
            if problem_type == "binary_classification":
                alter_query = f""" CREATE OR REPLACE TABLE `{model_table.name}`  AS
                        SELECT * EXCEPT({old_prediction_col}, {old_prediction_score_col} {indexes_except}) {indexes_as}, {old_prediction_col} as {prediction_col}, 
                        {old_prediction_score_col} as {prediction_score_col} 
                        FROM `{model_table.name}`"""
                query_job = bqc.query(alter_query)
                query_job.result()
            if problem_type == "regression":
                alter_query = f""" CREATE OR REPLACE TABLE `{model_table.name}`  AS
                        SELECT * EXCEPT({old_prediction_col} {indexes_except}) {indexes_as}, {old_prediction_col} as {prediction_col}
                        FROM `{model_table.name}`"""

                query_job = bqc.query(alter_query)
                query_job.result()

    def create_project_schema(self):
        if self.db_schema == None:
            raise InvalidArgumentError("schema_name is required")

        with BigQueryClient(self.data_store) as (client, _, _):
            dataset_id = "{}.{}".format(client.project, self.db_schema)

            try:
                client.get_dataset(dataset_id)  # Make an API request.
            except NotFound:
                logging.debug("Dataset {} is not found".format(dataset_id))
                # Construct a full Dataset object to send to the API.
                dataset = bigquery.Dataset(dataset_id)
                dataset.location = "US"

                # Send the dataset to the API for creation, with an explicit timeout.
                # Raises google.api_core.exceptions.Conflict if the Dataset already
                # exists within the project.
                dataset = client.create_dataset(
                    dataset, timeout=30
                )  # Make an API request.
        return

    def get_database_names(self):
        with BigQueryClient(self.data_store) as (client, _, _):
            projects = []
            for d in client.list_projects():
                projects.append(d.project_id)
            return projects

    def get_schema_names(self, database):
        with BigQueryClient(self.data_store) as (client, _, _):
            schemas = []
            for d in client.list_datasets(project=client.project):
                schemas.append(d.dataset_id)

            return schemas

    def get_table_names(self, database, schema):
        with BigQueryClient(self.data_store) as (client, _, _):
            tables = []
            for d in client.list_tables(dataset=schema):
                tables.append(d.table_id)

            return tables

    def get_column_names(self, database, schema, table):
        columns = []
        type_map = {}
        result_proxy = self.connection.execute(
            "SELECT column_name, data_type FROM {}.{}.INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}'".format(
                database, schema, table
            )
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            columns.append(d["column_name"])
            if "data_type" in d:
                type_map[d["column_name"]] = d["data_type"]

        return columns, type_map

    def load_data(self, filename, table_name, replace=False):
        with BigQueryClient(self.data_store) as (_, bqproject, key_file_name):
            if bqproject is None:
                return bigquery.Client()

            credentials = service_account.Credentials.from_service_account_file(
                key_file_name,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            source = FeatureSourceCloudStore(str(uuid.uuid4()), filename)
            df = source.fetch_all()
            exists = "fail"
            if replace:
                exists = "replace"
            name = "{}.{}".format(self.db_schema, table_name)
            try:
                df.to_gbq(
                    name,
                    project_id=bqproject,
                    chunksize=10000,
                    if_exists=exists,
                    credentials=credentials,
                )
            except ValueError:
                traceback.print_exc()
                raise

            return table_name

    def infer_schema(
        self,
        query,
        excludes=None,
        sample_row_count=100,
        allow_invalid_types=False,
        timeout_ms=0,
    ):
        inferred_schema = {}
        all_rows = []
        with BigQueryClient(self.data_store) as (client, _, _):
            if is_select_query(query):
                query = create_limit_query(query, sample_row_count or 100)
            logging.debug("About to run query: {}".format(query))
            query_job = client.query(query)
            res = query_job.result()

            columns = query_job._query_results._properties["schema"]["fields"]
            for col in columns:
                col_name = col["name"].lower()
                if excludes and col_name in excludes:
                    continue
                dtype = col["type"]
                if allow_invalid_types and dtype not in self.DTYPE_TO_LOGICAL:
                    inferred_schema[col_name] = {
                        "type": "INVALID",
                        "dtype": dtype,
                    }
                elif dtype in self.DTYPE_TO_LOGICAL:
                    inferred_schema[col_name] = {
                        "type": self.DTYPE_TO_LOGICAL[dtype],
                        "dtype": dtype,
                    }

            for row in res:
                drows = dict(row)
                # Filter our columns in the exclude list.
                if excludes is not None:
                    for e in excludes:
                        if e in drows:
                            del drows[e]

                all_rows.append(dumps(drows, default=str))
                if len(all_rows) >= sample_row_count:
                    break

        return inferred_schema, all_rows

    def _process_dataframe(
        self, df, id_column_name, ts_column_name, name, model_version
    ):
        for col in df.columns:
            if col.startswith("Unnamed:"):
                df = df.drop(col, axis=1)

        df.columns = map(str.lower, df.columns)
        # new query object should support better implementation
        for col in df.columns:
            if col.endswith(f":{id_column_name}"):
                df = df.rename(columns={col: id_column_name})
            if col.endswith(f":{ts_column_name}"):
                df = df.rename(columns={col: ts_column_name})

        df["batch_prediction"] = name
        df["model_version"] = model_version

        df = df.where(pd.notnull(df), None)

        return df

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
        logging.debug("in write_prediction")
        if self.data_store is None:
            logging.debug("skipping write_prediction")
            return

        project_id, pred_table = self.get_model_prediction_table_name(model)
        df = self._process_dataframe(
            df, id_column_name, ts_column_name, job_name, model_version
        )

        df["prediction_time"] = job_start_time
        full_name = f"{self.db_schema}.{pred_table}"

        with BigQueryClient(self.data_store) as (client, bqproject, key_file_name):
            credentials = service_account.Credentials.from_service_account_file(
                key_file_name,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            ## Insert into bigquery
            logging.info("df columns: {}".format(df.columns))
            logging.info("df columns dtypes: {}".format(df.dtypes))
            logging.info("full_name: {}".format(full_name))
            logging.info("time_index_dtype: {}".format(time_index_dtype))

            table_schema = []
            if time_index_dtype != None and (
                time_index_dtype == "DATE"
                or time_index_dtype == "DATETIME"
                or time_index_dtype == "TIME"
            ):
                table_schema.append({"name": ts_column_name, "type": time_index_dtype})
                logging.info(
                    "updated ts_column_name type to: {}".format(time_index_dtype)
                )

            df.to_gbq(
                full_name,
                bqproject,
                chunksize=None,
                if_exists="append",
                credentials=credentials,
                table_schema=table_schema,
            )

            count_query = f"SELECT COUNT(1) from `{self.db_schema}.{pred_table}` WHERE batch_prediction = '{job_name}'"
            res = client.query(count_query)
            for row in res:
                return row[0]
            return 0
