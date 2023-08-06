import logging
import traceback
import pandas as pd
import json
from datetime import datetime
from dateutil.parser import parse

import uuid
import grpc

from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict

from continual.python.utils import config
from continual.python.sdk.exceptions import InvalidArgumentError
from continual.rpc.dataingest.v1 import dataingest_pb2
from continual.rpc.dataingest.v1 import dataingest_pb2_grpc

from continual.rpc.management.v1 import management_types_pb2
from continual.services.dataingest.gcs_source import FeatureSourceCloudStore
from continual.python.sdk.features.schema_utils import get_type_enum
from continual.python.sdk.features.featurestore import get_featurestore
from continual.python.sdk.query import Query
from continual.python.sdk.datasets import Dataset

ProtoTypeMap = {
    "NUMBER": management_types_pb2.FieldType.NUMBER,
    "TEXT": management_types_pb2.FieldType.TEXT,
    "BOOLEAN": management_types_pb2.FieldType.BOOLEAN,
    "CATEGORICAL": management_types_pb2.FieldType.CATEGORICAL,
    "TIMESTAMP": management_types_pb2.FieldType.TIMESTAMP,
    "DATE": management_types_pb2.FieldType.DATE,
}

ERROR_NO_ID = "Row missing id column."


def collect_fields(qd, coll):
    for f in qd["fields"]:
        coll[f["qualified_name"]] = f["type"]
        if "relation" in f:
            collect_fields(f["relation"], coll)

    if "related" in qd:
        for r in qd["related"]:
            collect_fields(r, coll)


class DataIngestService(dataingest_pb2_grpc.DataIngestAPIServicer):
    def __init__(self):
        self._cfg = config.get_config("dataingest")
        self.jobs = {}

    def cfg(self, context: grpc.ServicerContext = None) -> dict:
        if not context:
            return self._cfg or dict()

        cfg = dict()
        cfg.update(self._cfg or dict())

        context_dict = dict(context.invocation_metadata() or {})
        cfg.update(context_dict or dict())

        return cfg

    def _build_feature_to_proto(self, df, feature_map):
        """
        match DF to schema
        """
        all_records = []
        for key in df.columns:
            if key not in feature_map:
                continue

            series = df[key]
            if len(series.shape) > 1:
                series = df[key].iloc[:, 0]

            if feature_map[key] == "TEXT" or feature_map[key] == "categorical":
                df[key] = series.astype(str, errors="ignore")
            if feature_map[key] == "NUMBER":
                df[key] = pd.to_numeric(series, errors="coerce")
            if feature_map[key] == "BOOLEAN":
                df[key] = series.astype(bool, errors="ignore")
            if feature_map[key] == "TIMESTAMP":
                df[key] = series.dt.to_pydatetime()

        record_dict = df.to_dict(orient="record")

        error_rows = 0
        for r in record_dict:
            try:
                features_record = json.dumps(r, default=str)
                all_records.append(features_record)
            except Exception:
                error_rows = error_rows + 1
                traceback.print_exc()
                continue

        return all_records

    def GetInferredSchema(self, request, context):
        logging.debug("Got GetInferredSchema")

        source_cfg = management_types_pb2.SourceConfig(
            query=request.query, file=request.file
        )

        sample_row_count = request.sample_row_count
        if sample_row_count is None:
            sample_row_count = 100

        try:
            source = None
            if request.table_name is not None and request.table_name != "":
                source = get_featurestore(
                    request.environment.data_store,
                    cfg=self.cfg(context),
                )
                inferred_schema, all_records = source.infer_schema(
                    f"SELECT * FROM {request.table_name}",
                    sample_row_count=sample_row_count,
                    allow_invalid_types=request.allow_invalid_types,
                )

            elif request.query is not None and request.query != "":
                source = get_featurestore(
                    request.environment.data_store,
                    cfg=self.cfg(context),
                )
                inferred_schema, all_records = source.infer_schema(
                    request.query,
                    sample_row_count=sample_row_count,
                    allow_invalid_types=request.allow_invalid_types,
                )
            else:
                uid = str(uuid.uuid1())
                logging.info(
                    "for project "
                    + request.project.name
                    + " attempt to download "
                    + request.file
                )
                source = FeatureSourceCloudStore(uid, None)
                inferred_schema, all_records = source.infer_schema(
                    request.file,
                    sample_row_count=sample_row_count,
                    allow_invalid_types=request.allow_invalid_types,
                )

            features = []

            for sc in inferred_schema:
                fs = management_types_pb2.ColumnConfig(
                    name=sc,
                    type=inferred_schema[sc]["type"],
                    dtype=inferred_schema[sc]["dtype"],
                )
                features.append(fs)

            resp = dataingest_pb2.GetInferredSchemaResponse(
                columns=features,
                record_count=len(all_records),
                values=all_records,
            )

            return resp

        except Exception as e:
            traceback.print_exc()
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return dataingest_pb2.GetInferredSchemaResponse()

    def GetData(self, request, context):
        logging.debug("Got GetData")
        fs = get_featurestore(
            request.data_store,
            cfg=self.cfg(context),
        )

        feature_map = {}
        index = None
        index_type = None
        for sc in request.columns:
            feature_map[sc.name] = sc.dtype
            if sc.type == management_types_pb2.FieldType.INDEX:
                index = sc
                index_type = sc.type

        if index is None:
            context.set_details("Invalid featureset, no index present")
            context.set_code(grpc.StatusCode.INTERNAL)
            return dataingest_pb2.GetDataResponse()

        token = request.page_token
        if index_type == ProtoTypeMap["NUMBER"]:
            token = float(request.page_token)
        elif index_type == ProtoTypeMap["TIMESTAMP"]:
            token = parse(request.page_token)
        else:
            if token == "":
                token = None

        df = fs.fetch_feature_data(
            name=request.name,
            index=index.name,
            page_size=request.page_size,
            page_token=token,
            table_name=request.table_name,
        )

        next_token = ""
        all_records = []
        if df.shape[0] != 0:
            next_token = str(df[index.name].values[-1])
            all_records = self._build_feature_to_proto(df, feature_map)

        resp = dataingest_pb2.GetDataResponse(
            record_count=len(all_records),
            next_page_token=next_token,
            value=all_records,
        )

        return resp

    def FormQuery(self, request, context):
        fs_map = {}
        for fs in request.feature_sets:
            fs_map[fs.name] = fs

        q = Query.form_query(
            model=request.model,
            all_featuresets=fs_map,
            metadata=request.add_metadata,
        )

        logging.debug(q)
        return q.to_proto()

    def GetServingData(self, request, context):
        logging.debug("Got GetServingData")
        fs = get_featurestore(
            request.data_store,
            cfg=self.cfg(context),
        )
        q_dict = MessageToDict(request.query, preserving_proto_field_name=True)
        overrides = json.loads(request.overrides)

        feature_map = {}
        collect_fields(q_dict, feature_map)

        query = Query(request.query)
        df = fs.fetch_serving_data(query, overrides)
        all_records = self._build_feature_to_proto(df, feature_map)
        resp = dataingest_pb2.GetServingDataResponse(
            value=all_records,
        )
        return resp

    def GetTrainingData(self, request, context):
        logging.debug("Got GetTrainingData")
        fs = get_featurestore(
            request.data_store,
            cfg=self.cfg(context),
        )
        q_dict = MessageToDict(request.query, preserving_proto_field_name=True)

        feature_map = {}
        collect_fields(q_dict, feature_map)

        all_records = []
        query = Query(request.query)
        df_iter = fs.fetch_training_data(query, n=3000)
        try:
            if isinstance(df_iter, pd.DataFrame):
                all_records.extend(self._build_feature_to_proto(df_iter, feature_map))
            else:
                for df in df_iter:
                    all_records.extend(self._build_feature_to_proto(df, feature_map))

                    # TODO: For now we only return first batch.
                    break
        except StopIteration:
            pass

        resp = dataingest_pb2.GetTrainingDataResponse(
            value=all_records,
        )
        return resp

    def ComputeStats(self, request, context):
        logging.debug("ComputeStats: ")
        fstore = get_featurestore(
            request.environment.data_store,
            cfg=self.cfg(context),
        )

        num_rows, computed_at, features = fstore.compute_feature_stats(
            request.name, request.columns, request.table_name
        )
        pb_features = []
        for f in features:
            for key, item in f.items():
                if isinstance(item, datetime):
                    dt = Timestamp()
                    dt.FromDatetime(item)
                    f[key] = dt
            f["type"] = get_type_enum(f.get("type", None))

            pb_features.append(management_types_pb2.ColumnStats(**f))

        timestamp = Timestamp()
        timestamp.FromDatetime(computed_at)
        fss = management_types_pb2.ColumnSetStats(
            name=request.name,
            row_count=num_rows,
            computed_at=timestamp,
            columns=pb_features,
        )
        resp = dataingest_pb2.ComputeStatsResponse(column_set_stats=fss)
        return resp

    def CreateFeatureSetTables(self, request, context):
        logging.debug("CreateFeatureSetTables: ")
        fstore = get_featurestore(
            request.environment.data_store,
            cfg=self.cfg(context),
        )

        fstore.create_feature_table(request.feature_set)
        return empty_pb2.Empty()

    def CreateModelTables(self, request, context):
        logging.debug("CreateModelTables: ")
        fstore = get_featurestore(
            request.environment.data_store,
            cfg=self.cfg(context),
        )

        fs_map = {}
        for fs in request.feature_sets:
            fs_map[fs.name] = fs

        problem_type = Dataset(
            model=request.model,
            featureset_map=fs_map,
            data_store=request.environment.data_store,
        ).inferred_problem_type

        fstore.create_model_tables(
            request.model,
            fs_map,
            problem_type,
            request.prev_index,
            request.prev_time_index,
        )
        return empty_pb2.Empty()

    def CreateFeatureStore(self, request, context):
        logging.debug("CreateFeatureStore: ")
        fstore = get_featurestore(
            request.environment.data_store, cfg=self.cfg(context), init=False
        )
        splits = request.environment.name.split("/")
        if len(splits) != 2:
            raise InvalidArgumentError(
                "Project name [{}] incorrect".format(request.environment.name)
            )

        fstore.create_project_schema()
        return empty_pb2.Empty()

    def CleanupFeatureTables(self, request, context):
        logging.debug("CleanupFeatureTablesRequest: ")
        fstore = get_featurestore(
            request.environment.data_store,
            cfg=self.cfg(context),
        )

        if "featureSet" in request.name:
            fstore.drop_featureset_view(request.name)
        elif "models" in request.name:
            fstore.drop_model_views(request.name)

        return empty_pb2.Empty()

    def DeleteFeatureStore(self, request, context):
        logging.debug("DeleteFeatureStore: ")
        fstore = get_featurestore(
            request.environment.data_store,
            cfg=self.cfg(context),
        )
        splits = request.environment.name.split("/")
        if len(splits) != 2:
            raise InvalidArgumentError(
                "Project name [{}] incorrect".format(request.environment.name)
            )

        fstore.delete_project_schema(fstore.db_schema)
        return empty_pb2.Empty()

    def BrowseDataWarehouse(self, request, context):
        logging.debug("BrowseDataWarehouse: ")

        fstore = get_featurestore(request.data_store, cfg=self.cfg(context), init=False)
        resp_data = []
        type_map = None
        if request.object_type == dataingest_pb2.BrowseDataWarehouseRequest.DATABASE:
            resp_data = fstore.get_database_names()
        elif request.object_type == dataingest_pb2.BrowseDataWarehouseRequest.SCHEMA:
            resp_data = fstore.get_schema_names(request.database)
        elif request.object_type == dataingest_pb2.BrowseDataWarehouseRequest.TABLE:
            resp_data = fstore.get_table_names(request.database, request.schema)
        elif request.object_type == dataingest_pb2.BrowseDataWarehouseRequest.COLUMN:
            resp_data, type_map = fstore.get_column_names(
                request.database, request.schema, request.table
            )

        return dataingest_pb2.BrowseDataWarehouseResponse(
            names=resp_data, types=type_map
        )

    def Seed(self, request, context):
        logging.debug("Seed: ")
        fstore = get_featurestore(request.environment.data_store, cfg=self.cfg(context))

        table_name = fstore.load_data(
            request.file_path, request.table_name, replace=True
        )
        return dataingest_pb2.SeedResponse(
            schema_name=fstore.db_schema, table_name=table_name
        )
