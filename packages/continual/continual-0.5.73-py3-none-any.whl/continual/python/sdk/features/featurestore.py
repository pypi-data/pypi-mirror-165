import logging
from typing import Tuple
from google.protobuf.json_format import MessageToDict
import pandas as pd
import numpy as np
import os, psutil
import traceback
import uuid
import json
from datetime import datetime
import hashlib, json
import random
import simplejson

from abc import ABC, abstractclassmethod
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql.schema import MetaData, Table

from .query_templates import (
    create_serving_query,
    timestamp_template,
    get_index,
    get_time_index_field,
    join_decision_dict,
)
from .index_template import (
    create_training_query,
)

from .model_templates import create_model_view_query
from continual.services.dataingest.gcs_source import FeatureSourceCloudStore
from continual.python.sdk.exceptions import (
    InvalidArgumentError,
    FailedPreconditionError,
)
from continual.python.utils.utils import (
    create_limit_query,
    is_select_query,
    parse_feature_set_name,
)
from continual.rpc.management.v1 import management_types_pb2
from continual.python.sdk.query import Query
from .schema_utils import load_schemas, get_type_enum

# Map for continual typenames to the database types.
Typemap = {
    "FIXED": db.Float,
    "REAL": db.Float,
    "FLOAT": db.Float,
    "TEXT": db.Text,
    "DATE": db.Date,
    "DATETIME": db.DateTime,
    "TIMESTAMP": db.TIMESTAMP(),
    "VARIANT": db.Text,
    "TIMESTAMP_LTZ": db.TIMESTAMP(timezone=True),
    "TIMESTAMP_TZ": db.TIMESTAMP(timezone=True),
    "TIMESTAMP_NTZ": db.TIMESTAMP(),
    "OBJECT": db.Text,
    "STRING": db.Text,
    "ARRAY": db.ARRAY(db.Text),
    "BINARY": db.LargeBinary,
    "TIME": db.TIMESTAMP,
    "BOOLEAN": db.BOOLEAN,
    "BOOL": db.BOOLEAN,
    "NUMBER": db.Float,
    "FLOAT64": db.Float,
    "INTEGER": db.Integer,
    "INT": db.Integer,
    "INT64": db.Integer,
    "SMALLINT": db.Integer,
    "SMALLINT": db.Integer,
    "TINYINT": db.Integer,
    "NUMERIC": db.Float,
    "DECIMAL": db.Float,
    "BIGNUMERIC": db.Float,
    "BIGDECIMAL": db.Float,
}

featurestore_cache = {}


class FilterTables:
    def __init__(self, schema=None):
        self.schema = schema

    def __call__(self, table_name, meta_data):
        if "test_permissions_" in table_name:
            return False
        if self.schema is not None:
            if not table_name.startswith(f"{self.schema}."):
                return False
        return True


def join_conditions(left_id, right_id, left_ts, right_ts):
    des = join_decision_dict.get(
        (
            left_id is not None,
            left_ts is not None,
            right_id is not None,
            right_ts is not None,
        ),
        "invalid",
    )
    if des == "invalid":
        raise Exception("Invalid join condition")
    elif des == "ID":
        return left_id, right_id, None, None
    elif des == "TS":
        return left_ts, right_ts, None, None

    return left_ts, right_ts, left_id, right_id


class FeatureStore(ABC):
    def __init__(self, projectid=None):
        self.projectid = projectid
        self.featuresets = {}
        self.models = {}
        self.db_schema = None

    def _get_table_name(self, name):
        comps = parse_feature_set_name(name)
        if "projects" not in comps or (
            "featureSets" not in comps and "models" not in comps
        ):
            # TODO: Throw exception.
            pass

        table_name = ""
        if "featureSets" in comps:
            table_name = comps["featureSets"]
        else:
            table_name = comps["models"]

        project_name = comps["projects"]
        if "@" in project_name:
            project_name = project_name.replace("@", "_")
        return project_name, table_name

    def get_data_table_name(self, name):
        project, table_name = self._get_table_name(name)
        comps = parse_feature_set_name(name)
        if "models" in comps:
            table_name = "model_{}".format(table_name)
        if "featureSets" in comps:
            table_name = "featureset_{}".format(table_name)
        return project, table_name

    def get_table_name(self, schema):
        return self._get_table_name(schema.name)

    def get_ingesting_table_name(self, feature_set):
        proj, table_name = self.get_table_name(feature_set)
        return proj, table_name + "_ingesting"

    def get_model_prediction_table_name(self, model):
        proj, table_name = self.get_table_name(model)
        proj = proj.replace("@", "_")
        return proj, "model_{}_predictions_history".format(table_name)

    def get_model_view_name(self, model):
        proj, table_name = self.get_table_name(model)
        return proj, "model_{}_predictions".format(table_name)

    def create_project_schema(self):
        if not self.db_schema:
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
        except Exception as e:
            logging.info(f"create schema exception: {e}")
            logging.info("schema does not appear to exist - create")
            self.connection.execute(
                "CREATE SCHEMA IF NOT EXISTS {}".format(self.db_schema)
            )

    def delete_project_schema(self, schema_name):
        self.connection.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(schema_name))

    def create_feature_table(self, feature_set):
        """
         Creates featuretable.
         This does not check for the existance of the featuretable and should
           be done prior to calling this.

        Args: Feature set for which the tables are to be created.
        Returns None
        """
        if feature_set.schema.query is not None and feature_set.schema.query != "":
            self.create_featureset_view(feature_set)
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

    def create_model_tables(
        self, model, featureset_map, problem_type, prev_index, prev_time_index
    ):
        logging.info("create_model_tables: {}".format(model))
        if model.schema.query is not None and model.schema.query != "":
            self.create_model_data_view(model)

        # Create all the historical prediction tables.
        self.create_prediction_model_table(
            model, problem_type, prev_index, prev_time_index
        )
        self.create_model_view(model, featureset_map, True, problem_type)

    def set_db_schema(self, db_schema):
        self.db_schema = db_schema

    def create_model_view(self, model, fs_map, metadata, problem_type):
        """
        Create or refresh model historical prediction tables and a view that
          joins training data and predictions.
        """

        _, entity_name = self.get_data_table_name(model.name)
        table_name = model.schema.table
        if table_name is None or table_name == "":
            table_name = f"{self.db_schema}.{entity_name}"

        index = model.schema.index or None
        time_index = model.schema.time_index or None
        for f in model.schema.columns:
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
        logging.info(model_query)
        try:
            self.connection.execute(model_query)
        except StopIteration:
            pass
        except:
            logging.info(traceback.format_exc()[:3000])
            raise

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
        meta = db.MetaData(schema=self.db_schema)

        meta.reflect(bind=self.engine, only=FilterTables())
        _, model_pred_name = self.get_model_prediction_table_name(model)
        model_table = None
        for t in meta.sorted_tables:
            if model_pred_name == t.name:
                model_table = t
        if model_table is None:
            self._create_prediction_model_table(
                model, model_pred_name, meta, problem_type
            )
        else:
            self._update_prediction_model_table(
                model, model_table, problem_type, prev_index, prev_time_index
            )

    def _update_prediction_model_table(
        self, model, model_table: Table, problem_type, prev_index, prev_time_index
    ):

        logging.info(f"update table: {model_table.name}")
        index_column = model.schema.index
        time_index_column = model.schema.time_index
        logging.info("index_column: {} prev: {}".format(index_column, prev_index))
        logging.info(
            "time_index_column: {} prev: {}".format(time_index_column, prev_time_index)
        )

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

        with self.connection.begin():
            if old_prediction_col != prediction_col:
                self.connection.execute(
                    f"ALTER TABLE {self.db_schema}.{model_table.name} RENAME COLUMN {old_prediction_col} TO {prediction_col}"
                )
                if old_prediction_details_col != "":
                    self.connection.execute(
                        f"ALTER TABLE {self.db_schema}.{model_table.name} RENAME COLUMN {old_prediction_details_col} TO {prediction_details_col}"
                    )
                if old_prediction_score_col != "":
                    self.connection.execute(
                        f"ALTER TABLE {self.db_schema}.{model_table.name} RENAME COLUMN {old_prediction_score_col} TO {prediction_score_col}"
                    )

            if prev_index != index_column and index_column != "":
                self.connection.execute(
                    f"ALTER TABLE {self.db_schema}.{model_table.name} RENAME COLUMN {prev_index} TO {index_column}"
                )
            if prev_time_index != time_index_column and time_index_column != "":
                self.connection.execute(
                    f"ALTER TABLE {self.db_schema}.{model_table.name} RENAME COLUMN {prev_time_index} TO {time_index_column}"
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

        columns = []
        columns.append(db.Column("batch_prediction", db.Text))
        columns.append(db.Column("model_version", db.Text))
        columns.append(db.Column("prediction_time", db.TIMESTAMP(timezone=True)))
        columns.append(db.Column(f"features", JSONB))

        if index is not None:
            columns.append(db.Column(index.name, Typemap[index.dtype]))

        if time_index is not None:
            columns.append(db.Column(time_index.name, Typemap[time_index.dtype]))
        columns.append(db.Column(f"{target_column}_prediction", target_column_dtype))
        if problem_type == "multiclass_classification":
            columns.append(db.Column(f"{target_column}_prediction_details", JSONB))
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
                logging.debug("Error while creating model table " + str(count))
                count = count + 1
                if count == 2:
                    raise

    def drop_table(self, table_name, view_name):
        logging.info("drop_table: " + table_name + " view: " + view_name)

        try:
            self.connection.execute(
                "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, view_name)
            )
        except:
            pass

        try:
            self.connection.execute(
                "DROP TABLE IF EXISTS {}.{}".format(self.db_schema, table_name)
            )
            return
        except StopIteration:
            pass
        except:
            logging.info(traceback.format_exc()[:3000])
            raise

    def load(self, dir_path):
        all_files = []
        if self.projectid is None:
            raise InvalidArgumentError("project needs to be set to load schemas")

        # r=root, d=directories, f = files
        for r, d, files in os.walk(dir_path):
            for f in files:
                if f.endswith(".yaml"):
                    all_files.append(os.path.join(r, f))

        count = 0
        for f in all_files:
            try:
                schema, schema_text = load_schemas(f)
                if schema is None:
                    print("Schema load failed")
                    continue

                if schema.query is not None and schema.query != "":
                    inferred, _ = self.infer_schema(schema.query, None, 0)
                    for col in schema.columns:
                        if col.name in inferred:
                            if col.name == "id" or col.name == schema.index:
                                col.type = management_types_pb2.FieldType.INDEX
                            # col.type = inferred[col.name]["type"]
                            col.dtype = inferred[col.name]["dtype"]
                            del inferred[col.name]

                    for col_name in inferred:
                        mc = management_types_pb2.ColumnConfig(
                            name=col_name,
                            type=get_type_enum(inferred[col_name].get("type", None)),
                            dtype=inferred[col_name]["dtype"],
                        )
                        schema.columns.append(mc)

                if schema.type == "FeatureSet":
                    fs = management_types_pb2.FeatureSet(
                        schema=schema, schema_text=schema_text
                    )
                    fs.name = (
                        "projects/" + self.projectid + "/featureSets/" + schema.name
                    )
                    self.featuresets[fs.name] = fs
                    if schema.table is None or schema.table == "":
                        self.create_feature_table(fs)

                    count = count + 1
                elif schema.type == "Model":
                    model = management_types_pb2.Model(
                        schema=schema, schema_text=schema_text
                    )
                    model.name = "projects/" + self.projectid + "/models/" + schema.name
                    self.models[model.name] = model
                    if (
                        schema.table is None
                        or schema.table == ""
                        and model.schema.target
                    ):
                        output_type = [
                            c.type
                            for c in model.schema.columns
                            if c.name == model.schema.target
                        ][0] or ""
                        problem_type = ""
                        if output_type == management_types_pb2.CATEGORICAL:
                            problem_type = "multiclass_classification"
                        if output_type == management_types_pb2.BOOLEAN:
                            problem_type = "binary_classification"
                        if output_type == management_types_pb2.NUMBER:
                            problem_type = "regression"
                        if output_type == management_types_pb2.TEXT:
                            problem_type = "text_prediction"
                        self.create_model_tables(
                            model, self.featuresets, problem_type, "", ""
                        )
                    else:
                        print("not creating model tables")
                    count = count + 1

            except Exception:
                raise
                # traceback.print_exc()

        return count

    def get_training_data(
        self,
        model,
        query=None,
        featureset_map=None,
        all_instances=False,
        latest=True,
        n=None,
        local=False,
    ):
        if featureset_map is None:
            featureset_map = self.featuresets

        if model is None:
            raise InvalidArgumentError("model required to get training data")

        if query is None:
            query = Query.form_query(
                model=model,
                all_featuresets=featureset_map,
            )

        df_iter = self.fetch_training_data(
            query.to_proto(),
            all_instances=all_instances,
            latest=latest,
            n=n,
            local=local,
        )

        return df_iter, query

    def create_featureset_view(self, feature_set):
        project, table_name = self.get_table_name(feature_set)
        table_name = "featureset_{}".format(table_name)
        query = feature_set.schema.query.strip().rstrip(";")
        create_query = "CREATE OR REPLACE VIEW {}.{} AS ({})".format(
            self.db_schema, table_name, query
        )
        logging.info(f"create_featureset_view query: {create_query}")
        self.connection.execute(create_query)

        return

    def create_model_data_view(self, model):
        _, table_name = self.get_data_table_name(model.name)
        query = model.schema.query.strip().rstrip(";")
        create_query = "CREATE OR REPLACE VIEW {}.{} AS ({})".format(
            self.db_schema, table_name, query
        )
        logging.info(f"create_model_data_view query: {create_query}")
        self.connection.execute(create_query)
        return

    def table_exists(self, schema_name, table_name):
        pass

    @abstractclassmethod
    def get_type(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def cleanup(self):
        raise NotImplementedError()

    @abstractclassmethod
    def is_hosted(self):
        raise NotImplementedError()

    @abstractclassmethod
    def close(self):
        raise NotImplementedError()

    @abstractclassmethod
    def get_stats_query_template(self):
        raise NotImplementedError()

    @abstractclassmethod
    def get_database_names(self):
        raise NotImplementedError()

    @abstractclassmethod
    def get_schema_names(self, database):
        raise NotImplementedError()

    @abstractclassmethod
    def get_table_names(self, database, schema):
        raise NotImplementedError()

    @abstractclassmethod
    def get_column_names(self, database, schema, table):
        raise NotImplementedError()

    @staticmethod
    def create_time_subquery(table_name, pkName, match_id, tsName, root_ts_name):
        params = {
            "EntityTable": table_name,
            "TsName": tsName,
            "PkName": pkName,
            "RootEntityID": match_id,
            "RootVisibilityTime": root_ts_name,
        }
        return timestamp_template.render(params=params)

    @staticmethod
    def create_featureset_query(
        name, db_schema, index, page_size=None, page_token=None, table_name=None
    ):
        parsed = parse_feature_set_name(name)
        if table_name is not None and table_name != "":
            full_name = table_name
        else:
            table_name = ""
            if "featureSets" in parsed:
                table_name = "featureset_" + parsed["featureSets"]
            else:
                table_name = "model_" + parsed["models"]

            full_name = db_schema + "." + table_name

        query = "SELECT * FROM {}".format(full_name)
        if page_token != None:
            if isinstance(page_token, str) and page_token != "":
                query = query + " WHERE {} > '{}'".format(str(index), str(page_token))
            else:
                query = query + " WHERE {} > {}".format(index, page_token)

        query = query + " ORDER BY {}".format(index)

        if page_size != None and page_size > 0:
            query = query + " LIMIT {}".format(page_size)

        return query

    def read_sql_query(
        self, query: str, chunksize: int = 1
    ) -> Tuple[pd.DataFrame, db.engine.ResultProxy]:
        """
        Slight rewrite of the Pandas SQL read_sql_query method. Instead of returning solely
        a DataFrame of the query results, this method will return the SQLAlchemy result proxy
        as well.
        """
        args = pd.io.sql._convert_params(query, None)

        pandas_sql = pd.io.sql.pandasSQL_builder(self.connection)
        result = pandas_sql.execute(*args)
        columns = result.keys()

        if chunksize is not None:
            return pandas_sql._query_iterator(result, chunksize, columns), result
        else:
            data = result.fetchall()
            frame = pd.io.sql._wrap_result(data, columns)
            return frame, result

    def infer_schema(
        self,
        query,
        excludes=None,
        sample_row_count=100,
        allow_invalid_types=False,
        timeout_ms=0,
    ):
        """
        Infers schema from the souce. Returns the schema as dictionary
         in following format.

        {
                 <feature_name> : <type>,
                 ...
             },
        """
        logging.info(f"infer_schema query: {query}")
        if is_select_query(query):
            query = create_limit_query(query, sample_row_count or 100)
        chunker, res = self.read_sql_query(query, chunksize=sample_row_count or 1)
        df = next(chunker)
        if excludes is not None:
            for c in excludes:
                if c in df.columns:
                    df = df.drop(c, axis=1)

        df.columns = [col.lower() for col in df.columns]
        inferred_schema = {}
        for col in df.select_dtypes(include=np.number).columns:
            colname = col.strip()
            if colname.startswith("unnammed:"):
                continue

            if len(colname) > 63:
                continue

            dtype = "FLOAT"
            if str(df[col].dtype).startswith("int"):
                dtype = "INTEGER"
            inferred_schema[colname] = {"type": "NUMBER", "dtype": dtype}

        for col in df.select_dtypes(include="object").columns:
            colname = col.strip()
            if colname.startswith("Unnammed:"):
                continue

            if len(colname) > 63:
                continue

            inferred_schema[colname] = {"type": "CATEGORICAL", "dtype": "TEXT"}

        for col in df.select_dtypes(include=["datetime", "datetimetz"]).columns:
            colname = col.strip()
            if colname.startswith("Unnammed:"):
                continue

            if len(colname) > 63:
                continue

            inferred_schema[colname] = {"type": "TIMESTAMP", "dtype": "TIMESTAMP"}

        for col in df.select_dtypes(include="bool").columns:
            colname = col.strip()
            if colname.startswith("Unnammed:"):
                continue

            if len(colname) > 63:
                continue

            inferred_schema[colname] = {"type": "BOOLEAN", "dtype": "BOOLEAN"}

        if allow_invalid_types and any(c not in inferred_schema for c in df.columns):
            type_codes = {c.name: c.type_code for c in res.cursor.description}
            types_df = pd.read_sql_query(
                "SELECT oid, typname FROM pg_type", self.connection
            )
            pg_types = {row[0]: row[1] for row in types_df.values}
            for col in df.columns:
                colname = col.strip()
                if colname.startswith("Unnammed:"):
                    continue
                if len(colname) > 63:
                    continue

                if colname not in inferred_schema and colname in type_codes:
                    inferred_schema[colname] = {
                        "type": "INVALID",
                        "dtype": pg_types.get(type_codes[colname], "INVALID"),
                    }

        all_records = []
        dicts = df.to_dict(orient="record")
        for d in dicts:
            all_records.append(simplejson.dumps(d, ignore_nan=True, default=str))
        return inferred_schema, all_records

    def fetch_feature_data(self, name, index, page_size, page_token, table_name):
        query = FeatureStore.create_featureset_query(
            name, self.db_schema, index, page_size, page_token, table_name
        )
        logging.info(query)
        return pd.read_sql_query(query, self.connection)

    def fetch_training_data(
        self,
        q,
        all_instances=False,
        n=None,
        local=False,
    ):
        if local:
            if isinstance(q, Query):
                qdict = q.to_dict()
            elif isinstance(q, management_types_pb2.Query):
                qdict = MessageToDict(q, preserving_proto_field_name=True)
            else:
                qdict = q

            return self.perform_local_join(qdict)

        """
        Returns a iterator for reading dataframes of traning data.
        """
        query, column_alias_map = create_training_query(
            q, self, all_instances=all_instances
        )
        logging.info(f"fetch_training_data query: {query}")
        if n == None:
            n = 100

        class CDFIter:
            def rename(self, df):
                df.rename(columns=self.mapping, inplace=True)
                return df

            def __init__(self, iterable, mapping):
                self.iterable = iterable
                self.mapping = mapping

            def __iter__(self):
                return self

            def __next__(self):
                ndf = next(self.iterable)
                return self.rename(ndf)

        return CDFIter(
            pd.read_sql_query(query, self.connection, chunksize=n), column_alias_map
        )

    def fetch_serving_data(self, q, overrides, data_store=None):
        """
        Returns a iterator for reading dataframes of traning data.
        """
        qd = q.override(overrides)
        if data_store is not None:
            data_store.get_type()
        query, params, sub_entities = create_serving_query(
            qd,
            False,
            self,
        )
        logging.info(query)
        df = pd.read_sql_query(query, self.connection)
        df.columns = df.columns.str.lower()
        if "finalrank" in df.columns:
            df = df.drop("finalrank", axis=1)

        for c in df.columns:
            if not c.endswith(".timerank"):
                continue
            df = df.drop(c, axis=1)

        return df

    def compute_feature_stats(self, name, columns, table_name=None):
        proj, entity_name = self.get_data_table_name(name)

        num_rows = 0
        features = []
        if table_name is None or table_name == "":
            table_name = f"{self.db_schema}.{entity_name}"

        res = self.connection.execute(f"SELECT count(*) as num_rows FROM {table_name}")
        row = next(res)
        num_rows = row[0]

        field_array = []  # TODO
        for f in columns:
            field_array.append(
                {
                    "name": f.name,
                    "type": f.dtype,
                    "ctype": management_types_pb2._FIELDTYPE.values_by_number[
                        f.type
                    ].name,
                }
            )

        params = {
            "AllFeatures": field_array,
            "FullName": table_name,
        }

        stats_query = self.get_stats_query_template().render(params=params)
        logging.info(stats_query)
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
            df.to_sql(
                table_name.lower(),
                self.connection,
                schema=self.db_schema,
                index=False,
                chunksize=10000,
                method="multi",
                if_exists=exists,
            )
        except ValueError:
            traceback.print_exc()

        return table_name.lower()

    def drop_featureset_view(self, name):
        project, table_name = self.get_data_table_name(name)
        self.connection.execute(
            "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, table_name)
        )
        return

    def drop_model_views(self, name):
        project, table_name = self._get_table_name(name)
        view_name = "model_{}_predictions".format(table_name)
        self.connection.execute(
            "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, view_name)
        )

        prediction_table_name = "model_{}_predictions_history".format(table_name)
        self.connection.execute(
            "DROP TABLE IF EXISTS {}.{}".format(self.db_schema, prediction_table_name)
        )

        project, table_name = self.get_data_table_name(name)
        self.connection.execute(
            "DROP VIEW IF EXISTS {}.{}".format(self.db_schema, table_name)
        )

        return

    def perform_local_join(self, q_dict):
        if q_dict is None:
            return None

        full_name = q_dict.get("table_name", None)

        project_id, table_name = self.get_data_table_name(q_dict["name"])
        if full_name is None:
            full_name = self.db_schema + "." + table_name

        df = pd.read_sql("select * from {}".format(full_name), self.engine)

        idx, qualified_idx = get_index(q_dict)
        time_idx, qualified_time_idx = get_time_index_field(q_dict)

        rename_dict = {}
        for field in q_dict["fields"]:
            rename_dict[field["name"]] = field["qualified_name"]
            if "type" in field and field["type"] == "TEXT":
                df[field["name"]] = df[field["name"]].astype("str")

            if "model" in field and field["model"]:
                df = df[df[field["name"]].notnull()]

            if "relation" in field and field["relation"] is not None:
                kdf = self.perform_local_join(field["relation"])
                r_idx, qualified_r_idx = get_index(field["relation"])
                r_time_idx, qualified_r_time_idx = get_time_index_field(
                    field["relation"]
                )

                logging.info(
                    "Join {} with {}".format(q_dict["name"], field["relation"]["name"])
                )
                left_on, right_on, left_by, right_by = join_conditions(
                    field["name"], qualified_r_idx, time_idx, qualified_r_time_idx
                )
                logging.info(
                    f"left_on {left_on}, right_on {right_on}, left_by {left_by}, right_by {right_by}"
                )
                df = df.sort_values(left_on)
                kdf = kdf.sort_values(right_on)
                if df.dtypes[left_on] != kdf.dtypes[right_on]:
                    raise FailedPreconditionError(
                        f"Unable to join data due to type mismatch: {left_on} {right_on}"
                    )

                if df.dtypes[left_on] == "O":
                    df = pd.merge(
                        df,
                        kdf,
                        left_on=left_on,
                        right_on=right_on,
                        suffixes=("", "_Continual"),
                        how="left",
                    )
                else:
                    df = pd.merge_asof(
                        df,
                        kdf,
                        left_on=left_on,
                        right_on=right_on,
                        left_by=left_by,
                        right_by=right_by,
                        suffixes=("", "_Continual"),
                        allow_exact_matches=True,
                    )
                del kdf

        if "related" in q_dict:
            for related in q_dict["related"]:
                kdf = self.perform_local_join(related)
                r_idx, qualified_r_idx = get_index(related)
                r_time_idx, qualified_r_time_idx = get_time_index_field(related)
                logging.info("Join {} with {}".format(q_dict["name"], related["name"]))
                left_on, right_on, left_by, right_by = join_conditions(
                    idx, qualified_r_idx, time_idx, qualified_r_time_idx
                )
                df = df.sort_values(left_on)
                kdf = kdf.sort_values(right_on)
                logging.info(
                    f"left_on {left_on}, right_on {right_on}, left_by {left_by}, right_by {right_by}"
                )
                if df.dtypes[left_on] != kdf.dtypes[right_on]:
                    raise FailedPreconditionError(
                        f"Unable to join data due to type mismatch: {left_on} {right_on}"
                    )

                if df.dtypes[left_on] == "O":
                    df = pd.merge(
                        df,
                        kdf,
                        left_on=left_on,
                        right_on=right_on,
                        suffixes=("", "_Continual"),
                        how="left",
                    )
                else:
                    df = pd.merge_asof(
                        df,
                        kdf,
                        left_on=left_on,
                        right_on=right_on,
                        left_by=left_by,
                        right_by=right_by,
                        suffixes=("", "_Continual"),
                        allow_exact_matches=True,
                    )
                del kdf

        for col in set(df.columns):
            if col.endswith("_Continual"):
                df.drop(col, axis=1, inplace=True)

        df.rename(rename_dict, inplace=True, axis=1)
        logging.info("Returning {}, {}".format(q_dict["name"], df.shape))
        process = psutil.Process(os.getpid())
        logging.info(
            "Current memory usage : {}".format(process.memory_info().rss / 1024 / 1024)
        )
        return df


def data_store_hash(datastore) -> str:
    """MD5 hash of a datastore."""
    if datastore is None:
        return "default"
    dictionary = MessageToDict(datastore)
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def get_cached(data_store):
    key = data_store_hash(data_store)
    fs_entry = featurestore_cache.get(key, None)
    if fs_entry is None:
        return None

    if (datetime.now() - fs_entry["access_time"]).seconds > 3600:
        del featurestore_cache[key]
        return None

    return fs_entry["featurestore"]


def update_cache(data_store, featurestore):
    key = data_store_hash(data_store)
    fs_entry = featurestore_cache.get(key, None)
    if fs_entry is None:
        featurestore_cache[key] = {
            "featurestore": featurestore,
            "access_time": datetime.now(),
        }


def get_datastore_db_schema(data_store: management_types_pb2.DataStore = None):
    if data_store is not None:
        if data_store.type == "snowflake":
            return data_store.snowflake.db_schema
        elif data_store.type == "sqlserver":
            return data_store.sqlserver.db_schema
        elif data_store.type == "continual" or data_store.type == "postgres":
            return data_store.postgres.db_schema
        elif data_store.type == "bigquery":
            return data_store.big_query.dataset
        elif data_store.type == "redshift":
            return data_store.redshift.db_schema
        elif data_store.type == "databricks":
            return data_store.databricks.db_schema
    return ""


def get_featurestore(
    data_store: management_types_pb2.DataStore = None,
    cached: bool = False,
    cfg: dict = None,
    projectid=None,
    init=True,
) -> FeatureStore:
    """Get backing data store for feature store."""
    fs = None
    if cached:
        fs = get_cached(data_store)

    if fs is None:
        if data_store is not None and data_store.type != "":
            if data_store.type == "snowflake":
                from .snowflake import SnowflakeFeatureStore

                fs = SnowflakeFeatureStore(data_store, None, cfg)
            elif data_store.type == "sqlserver":
                from .mssqlserver import MSSqlFeatureStore

                fs = MSSqlFeatureStore(data_store, None, cfg)
            elif data_store.type == "continual" or data_store.type == "postgres":
                from .postgres import PostgresFeatureStore

                fs = PostgresFeatureStore(data_store, None, cfg)
            elif data_store.type == "bigquery":
                from .bigquery import BigqueryFeatureStore

                fs = BigqueryFeatureStore(data_store, None, cfg)
            elif data_store.type == "redshift":
                from .redshift import RedshiftFeatureStore

                fs = RedshiftFeatureStore(data_store, None, cfg)
            elif data_store.type == "databricks":
                from .databricks import DatabricksFeatureStore

                fs = DatabricksFeatureStore(data_store, None, cfg, revive_cluster=init)
        else:
            # for testing purposes only
            logging.info("initializing postgres featurestore for testing")
            from .postgres import PostgresFeatureStore

            fs = PostgresFeatureStore(data_store, None, cfg)

            # create dummy data store
            data_store = management_types_pb2.DataStore()
            pg = management_types_pb2.DataStore.Postgres()
            data_store.type = "continual"
            data_store.postgres.MergeFrom(pg)
            data_store.postgres.db_schema = projectid or ""

    if fs is not None:
        update_cache(data_store, fs)

    fs.projectid = projectid
    logging.debug(f"setting fs projectid to {projectid or 'empty'}, init: {init}")

    if get_datastore_db_schema(data_store):
        fs.set_db_schema(get_datastore_db_schema(data_store))
        if not fs.projectid:
            fs.projectid = get_datastore_db_schema(data_store)
        if init:
            fs.create_project_schema()

    logging.debug("featurestore projectid: {}".format(fs.projectid))

    return fs
