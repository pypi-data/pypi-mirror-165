import sqlalchemy as db
import logging
import urllib
import traceback
from datetime import datetime
import pandas as pd
from sqlalchemy.exc import IntegrityError, ProgrammingError

from .prediction_store import PredictionStore, chunk_it
from .featurestore import FeatureStore, Typemap
from continual.python.sdk.exceptions import InvalidArgumentError
from continual.rpc.management.v1 import management_types_pb2
from .query_templates import stats_template_mssql


def create_connection(data_store):
    """
    Create mssql connection given data_store.
    """
    connection_string = "Driver={driver};Server=tcp:{host},{port};Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver="{ODBC Driver 17 for SQL Server}",
        host=data_store.host,
        port=data_store.port,
        database=data_store.database,
        user=data_store.username,
        password=data_store.password,
    )

    params = urllib.parse.quote_plus(connection_string)
    engine = db.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    connection = engine.connect()
    return engine, connection


class MSSqlFeatureStore(FeatureStore, PredictionStore):

    """
    MSSqlConnector implements both source of features and featurestore functions.

    Currently sources are not pooled. In a larger tenant with frequent and multiple fetches,
    we would need to consider connection pooling.
    """

    def __init__(self, data_store, source, cfg):
        self.data_store = data_store
        self.source = source
        self.corpus_id = None

        try:
            self.engine, self.connection = create_connection(data_store)
        except Exception:
            logging.debug(traceback.format_exc())
            raise InvalidArgumentError(
                "Connection to mssql failed, please check connection settings.",
                details=None,
            )
        super(MSSqlFeatureStore, self).__init__()

    def cleanup(self):
        tab_query = "select table_name, table_type from information_schema.tables where table_schema='{}'".format(
            self.db_schema
        )
        results = self.connection.execute(tab_query)
        views = []
        tables = []
        for row in results:
            if row[1] == "VIEW":
                views.append(row[0])
            else:
                tables.append(row[0])

        if len(tables) == 0:
            return

        # TODO: fix when/if we support mssqlserver
        logging.error("cleanup not supported for mlsqlserver")
        # with self.connection.begin():
        #     for table_name in tables:
        #         drop_table_query = "DROP TABLE {}.{}".format(project, table_name)
        #         self.connection.execute(drop_table_query)

        #     for table_name in views:
        #         drop_table_query = "DROP VIEW {}.{}".format(project, table_name)
        #         self.connection.execute(drop_table_query)

        #     drop_schema_query = "DROP SCHEMA {}".format(project)
        #     self.connection.execute(drop_schema_query)
        return

    def create_feature_table(self, feature_set):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.≈
        Returns None
        """
        for f in feature_set.schema.metadata:
            if (
                f.type == management_types_pb2.FieldType.NUMBER_LIST
                or f.type == management_types_pb2.FieldType.TEXT_LIST
            ):
                # Skip array types for mssql for now.
                return

        for f in feature_set.schema.features:
            if (
                f.type == management_types_pb2.FieldType.NUMBER_LIST
                or f.type == management_types_pb2.FieldType.TEXT_LIST
            ):
                # Skip array types for mssql for now.
                return

        for f in feature_set.schema.entities:
            if (
                f.type == management_types_pb2.FieldType.NUMBER_LIST
                or f.type == management_types_pb2.FieldType.TEXT_LIST
            ):
                # Skip array types for mssql for now.
                return

        for f in feature_set.schema.models:
            if (
                f.type == management_types_pb2.FieldType.NUMBER_LIST
                or f.type == management_types_pb2.FieldType.TEXT_LIST
            ):
                # Skip array types for mssql for now.
                return

        return super().create_feature_table(feature_set)

    def materialize_data(self, query):
        logging.info("Going to execute query " + query)
        results = self.connection.execute(query).fetchone()
        logging.info(results[0])
        return results[0]

    def fetch_data(self, page_start, page_size=100000, schema=None):
        # Not implemented
        return None

    def close(self):
        self.connection.close()

    def create_project_schema(self):
        results = self.connection.execute(
            "select count(*) from sys.schemas where name='{}'".format(self.db_schema)
        ).fetchone()
        if results[0] > 0:
            return
        self.connection.execute("CREATE SCHEMA {}".format(self.db_schema))

    def create_featureset_view(self, feature_set):
        project, table_name = self.get_table_name(feature_set)
        table_name = "featureset_{}".format(table_name)
        self.drop_table(table_name, "")

        query = feature_set.schema.source.query.strip().rstrip(";")
        self.connection.execute(
            "CREATE VIEW {}.{} AS ({})".format(project, table_name, query)
        )
        return

    def drop_table(self, table_name, view_name):
        archive_table_name = table_name + "_" + datetime.now().strftime("%Y%m%d%H%m%S")
        trans = self.connection.begin()
        try:
            self.connection.execute(
                """IF EXISTS (SELECT * from INFORMATION_SCHEMA.TABLES WHERE 
                                    table_schema='{}' and table_name='{}') 
                        BEGIN
                            EXEC sp_rename '{}', '{}'
                        END
                """.format(
                    self.db_schema,
                    table_name,
                    self.db_schema + "." + table_name,
                    archive_table_name,
                )
            )

            trans.commit()
        except:
            print(traceback.format_exc())
            logging.debug(traceback.format_exc())
            trans.rollback()
            raise

    def compute_feature_stats(self, featureset):
        proj, table_name = self.get_table_name(featureset)

        num_rows = 0
        features = []
        res = self.connection.execute(
            "SELECT count(*) as num_rows FROM {}.{}".format(proj, table_name)
        )
        row = next(res)
        num_rows = row[0]

        field_array = []  # TODO
        for f in featureset.schema.metadata:
            field_array.append(f)

        for f in featureset.schema.features:
            field_array.append(f)

        for f in featureset.schema.entities:
            field_array.append(f)

        for f in featureset.schema.models:
            field_array.append(f)

        params = {
            "SchemaName": featureset.name,
            "AllFeatures": field_array,
            "FullName": proj + "." + table_name,
            "Entity": featureset.schema.name,
        }

        stats_query = stats_template_mssql.render(params=params)
        cur = self.connection.execute(stats_query)
        done = False
        computed_at = None
        while not done:
            try:
                row = next(cur)
                d = dict(zip(row.keys(), row))
                if "computed_at" in d:
                    computed_at = d["computed_at"]
                    del d["computed_at"]

                features.append(d)
            except StopIteration:
                done = True

        return num_rows, computed_at, features

    def get_type(self) -> str:
        return "sqlserver"

    def is_hosted(self):
        return False

    def create_prediction_model_table(
        self, feature_set, model_id, prev_index, prev_time_index
    ):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.≈
        Returns None
        """
        project, table_name = self.get_table_name(feature_set)
        meta = db.MetaData(schema=project)

        index = None
        time_index = None
        for f in feature_set.schema.metadata:
            if f.index:
                index = f
            elif f.time_index:
                time_index = f

        _, model_pred_name = self.get_model_prediction_table_name(feature_set)

        columns = []
        columns.append(db.Column("batch_prediction_job", db.Text))
        columns.append(db.Column("model_version", db.Text))
        columns.append(db.Column("prediction_time", db.TIMESTAMP(timezone=True)))
        columns.append(db.Column(index.name, Typemap[index.type]))
        if time_index is not None:
            columns.append(db.Column(time_index.name, Typemap[time_index.type]))
        columns.append(db.Column("label", db.Text))
        columns.append(db.Column("category", db.Text))
        columns.append(db.Column("score", db.Float))
        columns.append(db.Column("details", db.Text))

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

    def get_stats_query_template(self):
        return stats_template_mssql

    def get_database_names(self):
        raise NotImplementedError()

    def get_schema_names(self, database):
        raise NotImplementedError()

    def get_table_names(self, database, schema):
        raise NotImplementedError()

    def get_column_names(self, database, schema, table):
        raise NotImplementedError()

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

        ch = chunk_it(0, df.shape[0])
        while ch is not None:
            df_slice = df[ch[0] : ch[1]]
            try:
                df_slice.to_sql(
                    pred_table,
                    self.connection,
                    schema=project_id,
                    if_exists="append",
                    index=False,
                )
            except:
                logging.info(traceback.format_exc()[:3000])
                raise

            ch = chunk_it(ch[1], df.shape[0])

        return 0
