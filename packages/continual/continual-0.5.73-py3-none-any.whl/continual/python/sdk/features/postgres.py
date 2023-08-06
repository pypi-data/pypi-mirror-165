import logging

import sqlalchemy as db
from sqlalchemy.exc import NoSuchTableError

from datetime import datetime
import json
import os
import traceback
import pandas as pd

from .query_templates import stats_template
from .featurestore import FeatureStore
from .prediction_store import PredictionStore, chunk_it


class PostgresFeatureStore(FeatureStore, PredictionStore):
    def __init__(self, data_store, source, cfg):
        self.data_store = data_store
        db_url = "postgresql://continual:continual@localhost:5432/continual"
        logging.info(f"PostgresFeatureStore data_store: {data_store}")
        try:
            if (
                data_store is None
                or data_store.postgres is None
                or data_store.postgres.host == ""
            ):
                if (
                    os.environ.get("CONFIG_ENV", "dev") != "test"
                    and "DatabaseURL" in cfg
                    and cfg["DatabaseURL"] is not None
                ):
                    db_url = cfg["DatabaseURL"]
            else:
                config = data_store.postgres
                db_url = "postgresql://{}:{}@{}:5432/{}".format(
                    config.username,
                    config.password,
                    config.host,
                    config.database,
                )
        except Exception as e:
            logging.error(
                "encountered error in postgres featurestore init: {}".format(e)
            )

        self.engine = db.create_engine(db_url)
        self.connection = self.engine.connect()
        self.trans = None
        super(PostgresFeatureStore, self).__init__()

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
        self.connection.execute("SET search_path TO {},public".format(db_schema))

    def cleanup(self):
        self.connection.execute("DROP SCHEMA IF EXISTS " + self.db_schema + " CASCADE")
        return

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_type(self) -> str:
        return "postgres"

    def is_hosted(self):
        return True

    def get_stats_query_template(self):
        return stats_template

    def get_database_names(self):
        raise NotImplementedError()

    def get_schema_names(self, database):
        raise NotImplementedError()

    def get_table_names(self, database, schema):
        raise NotImplementedError()

    def get_column_names(self, database, schema, table):
        raise NotImplementedError()

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
            df_slice["features"] = df_slice["features"].map(json.dumps)

            try:
                df_slice.to_sql(
                    pred_table,
                    self.connection,
                    schema=self.db_schema,
                    if_exists="append",
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
