import logging
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.exc import IntegrityError, ProgrammingError, NoSuchTableError
import urllib.parse

import traceback
import pandas as pd
import json
from datetime import datetime

from .query_templates import stats_template
from .featurestore import FeatureStore, Typemap
from .prediction_store import PredictionStore, chunk_it
from continual.rpc.management.v1 import management_types_pb2
from .model_templates import create_model_view_query
from sqlalchemy.sql.schema import MetaData


class RedshiftFeatureStore(FeatureStore, PredictionStore):
    def __init__(self, data_store, source, cfg):
        self.data_store = data_store
        config = data_store.redshift
        db_url = "postgresql://{}:{}@{}:{}/{}".format(
            config.username,
            urllib.parse.quote_plus(config.password),
            config.host,
            config.port,
            config.database,
        )

        self.engine = db.create_engine(db_url)
        self.connection = self.engine.connect()
        self.trans = None
        super(RedshiftFeatureStore, self).__init__()

    def create_feature_table(self, feature_set):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.≈
        Returns None
        """

        return super().create_feature_table(feature_set)

    def get_feature_table(self, feature_set):
        project, tablename = self.get_table_name(feature_set)
        tablename = "featureset_{}".format(tablename)
        try:
            tab = db.Table(
                tablename,
                db.MetaData(schema=self.db_schema),
                autoload=True,
                autoload_with=self.engine,
            )
            return tab
        except NoSuchTableError:
            print("No table found error")
            return None

    def set_db_schema(self, db_schema):
        self.db_schema = db_schema
        try:
            self.connection.execute("SET search_path TO {},public".format(db_schema))
        except:
            pass

    def cleanup(self):
        self.connection.execute("DROP SCHEMA IF EXISTS " + self.db_schema + " CASCADE")
        return

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_type(self) -> str:
        return "redshift"

    def is_hosted(self):
        return True

    def get_stats_query_template(self):
        return stats_template

    def get_database_names(self):
        databases = []
        result_proxy = self.connection.execute(
            "SELECT database_name as name FROM svv_redshift_databases ORDER BY name"
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            databases.append(d["name"])

        return databases

    def get_schema_names(self, database):
        schemas = []
        result_proxy = self.connection.execute(
            "SELECT schema_name as name FROM svv_redshift_schemas WHERE database_name = '{}' ORDER BY name".format(
                database
            )
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            if d["name"] == "INFORMATION_SCHEMA":
                continue
            schemas.append(d["name"])

        return schemas

    def get_table_names(self, database, schema, views=True):
        tables = []
        result_proxy = self.connection.execute(
            "SELECT table_name as name FROM svv_redshift_tables WHERE database_name = '{}' AND schema_name = '{}' ORDER BY name".format(
                database, schema
            )
        )
        for rowproxy in result_proxy:
            d = {}
            for col, val in rowproxy.items():
                d[col] = val
            tables.append(d["name"])

        if views:
            pass
            # result_proxy = self.connection.execute(
            #     "SHOW VIEWS IN SCHEMA {}.{}".format(database, schema)
            # )
            # for rowproxy in result_proxy:
            #     d = {}
            #     for col, val in rowproxy.items():
            #         d[col] = val
            #     tables.append(d["name"])
        return tables

    def get_column_names(self, database, schema, table):
        columns = []
        type_map = {}
        result_proxy = self.connection.execute(
            "SELECT column_name, data_type FROM svv_redshift_columns WHERE database_name = '{}' AND schema_name = '{}' AND table_name = '{}' ORDER BY column_name".format(
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
        columns.append(db.Column("prediction_time", db.TIMESTAMP(timezone=True)))
        columns.append(db.Column(f"features", VARCHAR(65535)))

        if index is not None:
            columns.append(db.Column(index.name, Typemap[index.dtype]))

        if time_index is not None:
            columns.append(db.Column(time_index.name, Typemap[time_index.dtype]))
        columns.append(db.Column(f"{target_column}_prediction", target_column_dtype))
        if problem_type == "multiclass_classification":
            columns.append(
                db.Column(f"{target_column}_prediction_details", VARCHAR(65535))
            )
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
        logging.debug(
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
        df["prediction_time"] = job_start_time.strftime("%Y-%m-%d %H:%M:%S")

        db_url = f"postgresql://{self.data_store.redshift.username}:{urllib.parse.quote_plus(self.data_store.redshift.password)}@{self.data_store.redshift.host}:{self.data_store.redshift.port}/{self.data_store.redshift.database}"
        self.engine = db.create_engine(db_url)
        self.connection = self.engine.connect()

        tab = self.get_prediction_table(model)
        if tab is None:
            print("Prediction table not found")
            logging.debug("Prediction table not found")
            return

        # set chained assignent to warn in case an underlying model has set to raise
        # TODO: determine if there's a better method of mapping the json values
        pd.set_option("mode.chained_assignment", "warn")
        trans = self.connection.begin()

        prediction_details_column = f"{output_name}_prediction_details"

        ch = chunk_it(0, df.shape[0])
        while ch is not None:
            df_slice = df[ch[0] : ch[1]]
            if prediction_details_column in df_slice.columns:
                df_slice[prediction_details_column] = df_slice[
                    prediction_details_column
                ].map(json.dumps)

            try:
                df_slice.to_sql(
                    pred_table,
                    self.connection,
                    schema=self.db_schema,
                    if_exists="append",
                    method="multi",
                    index=False,
                )
            except:
                trans.rollback()
                traceback.print_exc()
                logging.debug("write failed to execute - aborting")
                raise
            ch = chunk_it(ch[1], df.shape[0])

        trans.commit()

        count_query = f"SELECT COUNT(1) from {self.db_schema}.{pred_table} WHERE batch_prediction = '{job_name}'"
        result = self.connection.execute(count_query)
        for row in result:
            return row[0]
        return 0

    def create_view(self, feature_set):
        project, table_name = self.get_table_name(feature_set)

        # drop the view first if it exists
        self.connection.execute(
            "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, table_name)
        )

        query = feature_set.schema.query.strip().rstrip(";")
        self.connection.execute(
            "CREATE OR REPLACE VIEW {}.{} AS ({}) WITH NO SCHEMA BINDING".format(
                self.db_schema, table_name, query
            )
        )
        return

    def create_featureset_view(self, feature_set):
        project, table_name = self.get_table_name(feature_set)
        table_name = "featureset_{}".format(table_name)
        query = feature_set.schema.query.strip().rstrip(";")
        self.connection.execute(
            "CREATE OR REPLACE VIEW {}.{} AS ({}) WITH NO SCHEMA BINDING".format(
                self.db_schema, table_name, query
            )
        )
        return

    def create_model_data_view(self, model):
        project, table_name = self.get_data_table_name(model.name)

        # drop the view first if it exists
        self.connection.execute(
            "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, table_name)
        )

        query = model.schema.query.strip().rstrip(";")
        self.connection.execute(
            "CREATE OR REPLACE VIEW {}.{} AS ({}) WITH NO SCHEMA BINDING".format(
                self.db_schema, table_name, query
            )
        )
        return

    def create_model_view(self, model, fs_map, metadata, problem_type):
        """
        Create or refresh model historical prediction tables and a view that
          joins training data and predictions.
        """

        project, entity_name = self.get_data_table_name(model.name)
        table_name = model.schema.table
        if table_name is None or table_name == "":
            table_name = f"{self.db_schema}.{entity_name}"

        index = model.schema.index or None
        time_index = model.schema.time_index or None
        for f in model.schema.columns:
            logging.info(f"create_model_view column: {f}")
            if f.type == management_types_pb2.FieldType.INDEX:
                index = f.name
            elif f.type == management_types_pb2.FieldType.TIME_INDEX:
                time_index = f.name

        _, model_pred_name = self.get_model_prediction_table_name(model)
        proj, model_view_name = self.get_model_view_name(model)

        # The training data query returns qulified column names. in order to join this column name we need
        # to pass the name to be expected out of the traning query.
        index_match_name = index
        time_match_name = None
        if time_index:
            time_match_name = time_index

        model_query = create_model_view_query(
            table_name,
            index,
            time_index,
            index_match_name,
            time_match_name,
            model_pred_name,
            proj,
            model_view_name,
            model.schema.target,
            self.db_schema,
            problem_type,
        )
        # add redshift WITH NO SCHEMA BINDING
        model_query_final = f"{model_query} WITH NO SCHEMA BINDING"
        logging.info(model_query_final)
        try:
            # drop view first
            self.connection.execute(
                "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, model_view_name)
            )
            self.connection.execute(model_query_final)
        except StopIteration:
            pass
        except:
            logging.info(traceback.format_exc()[:3000])
            raise

    def infer_schema(
        self,
        query,
        excludes=None,
        sample_row_count=100,
        allow_invalid_types=False,
        timeout_ms=0,
    ):
        if timeout_ms and timeout_ms > 0:
            config = self.data_store.redshift
            db_url = "postgresql://{}:{}@{}:{}/{}".format(
                config.username,
                urllib.parse.quote_plus(config.password),
                config.host,
                config.port,
                config.database,
            )
            self.engine = db.create_engine(
                db_url,
                connect_args={"options": "-c statement_timeout={}".format(timeout_ms)},
            )
            self.connection = self.engine.connect()

            res = super().infer_schema(
                query, excludes, sample_row_count, allow_invalid_types, timeout_ms
            )

            self.engine = db.create_engine(db_url)
            self.connection = self.engine.connect()

            return res
        else:
            return super().infer_schema(
                query, excludes, sample_row_count, allow_invalid_types, timeout_ms
            )
