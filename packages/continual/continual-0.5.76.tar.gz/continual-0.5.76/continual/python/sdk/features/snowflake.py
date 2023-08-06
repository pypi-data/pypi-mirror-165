import sqlalchemy as db
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy import exc

import logging
import pandas as pd
import uuid
import re
from jinja2 import Template
from functools import wraps
import traceback
from json import loads, dumps
from datetime import datetime
import shortuuid

from snowflake.sqlalchemy import VARIANT
from sqlalchemy.sql.schema import MetaData
from snowflake.connector.constants import FIELD_ID_TO_NAME
from snowflake.connector import connect as snow_con
import snowflake.connector.pandas_tools as ptools
from snowflake.connector.errors import ProgrammingError as SFProgrammingError
from continual.python.utils.utils import is_select_query, create_limit_query

from continual.rpc.management.v1 import management_types_pb2
from .featurestore import FeatureStore, Typemap
from .prediction_store import PredictionStore
from continual.python.sdk.exceptions import InvalidArgumentError
from .query_templates import stats_template_snowflake
from continual.services.dataingest.gcs_source import FeatureSourceCloudStore


TABLE_NOT_FOUND_ERROR_MSG = "tables(s) not found. Check if there are double quotes around table or schema names. Snowflake considers quotes names as case sensitve"
insert_template = Template(
    """INSERT INTO  {{param.db_schema}}.{{param.table_name}} ({% for r in param.insert_list %}{%if loop.index0 != 0%},{% endif %}{{r}}{% endfor %})
        SELECT {% for r in param.columns %}{%if loop.index0 != 0%},{% endif %}{{r}}{% endfor %} 
        FROM {{param.db_schema}}.{{param.temp_table}}"""
)

COLUMN_STATS_BATCH = 250


def column_name_mapper(col_name):
    new_name = re.sub("[^a-zA-Z0-9_]", "_", col_name)
    return new_name.lower()


def create_incremental_query(query, columns, page_data):

    """
    A user given query is wrapped to perform incremental data extraction.

    Returns: sqlalchemy query statement object prepared for incremental data pull.
    """
    if columns is None or len(columns) == 0:
        return db.text(query)

    if page_data is None or len(page_data.keys()) == 0:
        return db.text(query)

    all_columns = []
    for col in columns:
        if col in page_data and page_data[col] is not None:
            all_columns.append(db.column(col))

    # Check if are able to do incremental ingest. If not do full ingest
    if len(all_columns) == 0:
        return db.text(query)

    # Prepare user given text query for use as a subquery.
    q2 = db.text(query).columns(*all_columns).alias("itr")

    # Wrap the user given query with column starts.
    # So a query q will be wraped as
    # SELECT * from (<q>) as itr where itr.<col1> > <cdata1> AND....
    q_full = select([db.text("*")])
    for col in columns:

        # Ignore columns for which we do not have start data.
        if col not in page_data or page_data[col] is None:
            continue
        cdata = page_data[col]
        q_full = q_full.where(q2.c[col] > cdata)

    return q_full


def handle_snowflake_exception(func):
    """Decorator that parses Snowflake exceptions raised through SQLAlchemy.

    Args:
        func: Function to wrap.
    Returns:
        A function that will raise an informative exception.
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SFProgrammingError as e:
            if e.msg.startswith("invalid identifier"):
                raise InvalidArgumentError(
                    message=f"{e.msg}, this can happen if the underlying table in snowflake has case sensitive column names",
                    details=None,
                )
        except exc.SQLAlchemyError as e:
            if isinstance(e, exc.ProgrammingError):
                msg = str(e.orig) or ""
                msg = msg.split("\n")[-1]
                if not msg:
                    msg = str(e.orig)
                if msg.startswith("invalid identifier"):
                    msg = f"{msg}, this can happen if the underlying table in snowflake has case sensitive column names"
                elif msg.startswith(
                    "Object does not exist, or operation cannot be performed"
                ):
                    msg = f"{msg}, Please check if you have sufficient permissions"
                raise InvalidArgumentError(message=msg, details=None)
            elif isinstance(e, exc.InvalidRequestError):
                msg = str(e)
                if "requested table(s) not available in Engine" in msg:
                    msg = TABLE_NOT_FOUND_ERROR_MSG
                raise InvalidArgumentError(message=msg, details=None)
            raise e
        except:
            raise

    return wrapped_func


def create_connection(data_store):
    """
    Create snowflake connection given data_store.
    """
    account = data_store.snowflake.host
    if account.endswith(".snowflakecomputing.com"):
        account = account[: len(account) - len(".snowflakecomputing.com")]

    engine_url = db.engine.URL.create(
        "snowflake",
        username=data_store.snowflake.username,
        password=data_store.snowflake.password,
        host=account,
        database=data_store.snowflake.database,
        query=dict(
            warehouse=data_store.snowflake.warehouse,
            role=data_store.snowflake.role,
            application="Continual",
        ),
    )

    sf_eng = db.create_engine(engine_url)

    connection = sf_eng.connect()
    # connection.execute("alter session set quoted_identifiers_ignore_case = true")
    return sf_eng, connection


class SnowflakeFeatureStore(FeatureStore, PredictionStore):

    """
    SnowflakeFeatureStore implements both source of features and featurestore functions.

    Currently sources are not pooled. In a larger tenant with frequent and multiple fetches,
    we would need to consider connection pooling.
    """

    DTYPE_TO_LOGICAL = {
        "FIXED": "NUMBER",
        "REAL": "NUMBER",
        "TEXT": "CATEGORICAL",
        "DATE": "TIMESTAMP",
        "TIMESTAMP": "TIMESTAMP",
        "VARIANT": "TEXT",
        "TIMESTAMP_LTZ": "TIMESTAMP",
        "TIMESTAMP_TZ": "TIMESTAMP",
        "TIMESTAMP_NTZ": "TIMESTAMP",
        "OBJECT": "TEXT",
        "ARRAY": "STRING_ARRAY",
        "BINARY": "TEXT",
        "TIME": "TIMESTAMP",
        "BOOLEAN": "BOOLEAN",
    }

    def __init__(self, data_store, source, cfg):
        self.data_store = data_store
        self.source = source
        self.corpus_id = None

        try:
            self.engine, self.connection = create_connection(data_store)
        except Exception:
            raise InvalidArgumentError(
                "Connection to Snowflake failed, please check connection settings.",
                details=None,
            )
        super(SnowflakeFeatureStore, self).__init__()

    def cleanup(self):
        print("Dropping ", self.db_schema)
        self.connection.execute("DROP SCHEMA IF EXISTS " + self.db_schema + " CASCADE")
        return

    @handle_snowflake_exception
    def create_project_schema(self):
        return super().create_project_schema()

    @handle_snowflake_exception
    def create_feature_table(self, feature_set):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.≈
        Returns None
        """
        return super().create_feature_table(feature_set)

    @handle_snowflake_exception
    def materialize_data(self, query):
        logging.info("Going to execute query " + query)
        results = self.connection.execute(query).fetchone()
        logging.info(results[0])
        return results[0]

    @handle_snowflake_exception
    def fetch_data(self, page_start, page_size=100000, schema=None):
        # TODO: fetch_data would be enhanced for batch gets with additional parameters.
        query = self.source.query.rstrip().rstrip(";")

        if (
            self.source.incremental_column is not None
            and self.source.incremental_column != ""
            and page_start is not None
        ):
            columns = [self.source.incremental_column]
            query = create_incremental_query(query, columns, page_start)

        logging.info(query)

        class DFIterator:
            def __init__(self, connection, query):
                self._connection = connection
                self._query = query
                self._current_index = 0
                self.chunker = None

            def __iter__(self):
                self.chunker = None
                return self

            def __next__(self):
                if self.chunker is not None:
                    return next(self.chunker)

                self.chunker = pd.read_sql(
                    self._query,
                    self._connection,
                    chunksize=page_size,
                )

                self._current_index = self._current_index + 1
                return next(self.chunker)

        return DFIterator(self.connection, query)

    @handle_snowflake_exception
    def infer_schema(
        self,
        query,
        excludes=None,
        sample_row_count=100,
        allow_invalid_types=False,
        timeout_ms=0,
    ):
        inferred_schema = {}
        if is_select_query(query):
            query = create_limit_query(query, sample_row_count)
        logging.info("about to execute query: {}".format(query))
        res = self.connection.execute(query)
        for j in res.cursor.description:
            col = j[0].lower()
            if excludes is not None and col in excludes:
                continue

            dtype = FIELD_ID_TO_NAME[j[1]]
            if allow_invalid_types and dtype not in self.DTYPE_TO_LOGICAL:
                inferred_schema[col] = {"type": "INVALID", "dtype": dtype}
            elif dtype in self.DTYPE_TO_LOGICAL:
                inferred_schema[col] = {
                    "type": self.DTYPE_TO_LOGICAL[dtype],
                    "dtype": dtype,
                }

        all_rows = []
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

    def set_db_schema(self, db_schema):
        db_schema_name = db_schema
        # if schema is the project name
        splits = db_schema.split("/")
        if len(splits) == 2:
            db_schema_name = splits[1]

        self.db_schema = db_schema_name
        # self.connection.execute("USE schema {}".format(db_schema))

    @handle_snowflake_exception
    def close(self):
        self.connection.close()

    @handle_snowflake_exception
    def drop_table(self, table_name, view_name):
        return super().drop_table(table_name, view_name)

    @handle_snowflake_exception
    def fetch_featureset_data(
        self,
        feature_set,
        index,
        page_size,
        page_token,
    ):
        return super().fetch_featureset_data(feature_set, index, page_size, page_token)

    @handle_snowflake_exception
    def fetch_training_data(
        self,
        q,
        all_instances=False,
        n=None,
        local=False,
    ):
        return super().fetch_training_data(
            q,
            all_instances,
            n,
            local=local,
        )

    @handle_snowflake_exception
    def fetch_serving_data(self, q, overrides, data_store=None):
        return super().fetch_serving_data(q, overrides=overrides, data_store=data_store)

    def get_type(self) -> str:
        return "snowflake"

    def is_hosted(self):
        return False

    def get_stats_query_template(self):
        return stats_template_snowflake

    @handle_snowflake_exception
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
        logging.info("snowflake: _create_prediction_model_table")
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
        columns.append(db.Column("prediction_time", db.TIMESTAMP(timezone=True)))
        columns.append(db.Column(f"features", VARIANT))

        if index is not None:
            columns.append(db.Column(index.name, Typemap[index.dtype]))

        if time_index is not None:
            columns.append(db.Column(time_index.name, Typemap[time_index.dtype]))
        columns.append(db.Column(f"{target_column}_prediction", target_column_dtype))

        if problem_type == "multiclass_classification":
            columns.append(db.Column(f"{target_column}_prediction_details", VARIANT))
            columns.append(db.Column(f"{target_column}_prediction_score", db.Float))
        if problem_type == "binary_classification":
            columns.append(
                db.Column(f"{target_column}_true_prediction_score", db.Float)
            )

        db.Table(model_pred_name, meta, *columns)

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

    @handle_snowflake_exception
    def get_database_names(self):
        databases = []
        result_proxy = self.connection.execute("SHOW DATABASES")
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            databases.append(d["name"])

        return databases

    @handle_snowflake_exception
    def get_schema_names(self, database):
        schemas = []
        result_proxy = self.connection.execute(
            "SHOW SCHEMAS IN DATABASE {}".format(database)
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            if d["name"] == "INFORMATION_SCHEMA":
                continue
            schemas.append(d["name"])

        return schemas

    @handle_snowflake_exception
    def get_table_names(self, database, schema, views=True):
        tables = []
        result_proxy = self.connection.execute(
            "SHOW TABLES IN SCHEMA {}.{}".format(database, schema)
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            tables.append(d["name"])

        if views:
            result_proxy = self.connection.execute(
                "SHOW VIEWS IN SCHEMA {}.{}".format(database, schema)
            )
            for rowproxy in result_proxy:
                d = {}
                for col, val in rowproxy.items():
                    d[col] = val
                tables.append(d["name"])
        return tables

    @handle_snowflake_exception
    def get_column_names(self, database, schema, table):
        columns = []
        type_map = {}
        result_proxy = self.connection.execute(
            "SHOW COLUMNS IN TABLE {}.{}.{}".format(database, schema, table)
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            columns.append(d["column_name"])
            if "data_type" in d:
                type_dict = loads(d["data_type"])
                type_map[d["column_name"]] = type_dict["type"]

        return columns, type_map

    @handle_snowflake_exception
    def compute_feature_stats(self, name, columns, table_name=None):
        if len(columns) <= COLUMN_STATS_BATCH:
            return super().compute_feature_stats(name, columns, table_name)

        num_rows = None
        computed_at = 0
        all_features = []
        i = 0
        j = COLUMN_STATS_BATCH
        while i < len(columns):
            logging.info("I {} J {}".format(i, j - 1))
            if num_rows is None:
                num_rows, computed_at, features = super().compute_feature_stats(
                    name, columns[i : j - 1], table_name
                )
            else:
                _, _, features = super().compute_feature_stats(
                    name, columns[i : j - 1], table_name
                )
            all_features.extend(features)
            i = j
            if j + COLUMN_STATS_BATCH >= len(columns):
                j = j + (len(columns) - j)
            else:
                j = j + COLUMN_STATS_BATCH
            if i == j:
                break

        logging.info("All-Features{} I {} J {}".format(len(all_features), i, j - 1))
        return num_rows, computed_at, all_features

    @handle_snowflake_exception
    def load_data(self, filename, table_name, replace=False):
        source = FeatureSourceCloudStore(str(uuid.uuid4()), filename)
        df = source.fetch_all()

        df = df.rename(column_name_mapper, axis=1)
        table_name = table_name.lower()
        df.head(0).to_sql(
            name=table_name,
            con=self.connection,
            schema=self.db_schema,
            if_exists="replace",
            index=False,
        )

        account = self.data_store.snowflake.host
        if account.endswith(".snowflakecomputing.com"):
            account = account[: len(account) - len(".snowflakecomputing.com")]

        with snow_con(
            account=account,
            user=self.data_store.snowflake.username,
            password=self.data_store.snowflake.password,
            database=self.data_store.snowflake.database,
            warehouse=self.data_store.snowflake.warehouse,
            role=self.data_store.snowflake.role,
            application="Continual",
        ) as con:
            con.cursor().execute(f"Use schema {self.db_schema}")
            ptools.write_pandas(
                con,
                df,
                database=self.data_store.snowflake.database,
                schema=self.db_schema,
                table_name=table_name,
                quote_identifiers=False,
            )
        return table_name

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
        df["prediction_time"] = job_start_time.strftime("%Y-%m-%d %H:%M:%S")

        temp_table_name = pred_table + "_" + shortuuid.uuid().lower()
        ## Insert into temp table.
        with snow_con(
            user=self.data_store.snowflake.username,
            password=self.data_store.snowflake.password,
            account=self.data_store.snowflake.host,
            database=self.data_store.snowflake.database,
            warehouse=self.data_store.snowflake.warehouse,
            role=self.data_store.snowflake.role,
            application="Continual",
        ) as con:
            con.cursor().execute(f"Use schema {self.db_schema}")
            con.cursor().execute(
                f"CREATE TEMP TABLE {self.db_schema}.{temp_table_name} LIKE {self.db_schema}.{pred_table}"
            )

            ptools.write_pandas(
                con,
                df,
                database=self.data_store.snowflake.database,
                schema=self.db_schema,
                table_name=temp_table_name,
                quote_identifiers=False,
            )

            all_columns = []
            insert_list = []

            for column in df.columns:
                insert_list.append(column)
                if column == "features":
                    all_columns.append("PARSE_JSON(features) as features")
                elif column.endswith("_details"):
                    all_columns.append(f"PARSE_JSON({column}) as {column}")
                else:
                    all_columns.append(column)

            logging.info("all columns: {}".format(all_columns))
            param = {
                "db_schema": self.db_schema,
                "temp_table": temp_table_name,
                "table_name": pred_table,
                "columns": all_columns,
                "insert_list": insert_list,
            }
            query = insert_template.render(param=param)
            logging.info("query: {}".format(query))
            con.cursor().execute(query)

            # get prediction count
            count_query = f"SELECT COUNT(1) from {self.db_schema}.{pred_table} WHERE batch_prediction = %s"
            count_cur = con.cursor()
            count_cur.execute(count_query, (job_name))
            res = count_cur.fetchone()
            return res[0]
