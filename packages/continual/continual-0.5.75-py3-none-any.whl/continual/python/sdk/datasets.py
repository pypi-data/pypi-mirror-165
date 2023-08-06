import pandas as pd
from typing import Dict, List
import logging
from continual.rpc.management.v1 import management_types_pb2, types
from continual.python.sdk.query import Query
from continual.python.sdk.features.featurestore import get_featurestore
from continual.services.compute_services.constants import POSTGRES_DB_URL


class Dataset:
    def __init__(
        self,
        model: management_types_pb2.Model,
        featureset_map: Dict[str, management_types_pb2.FeatureSet],
        data_store: management_types_pb2.DataStore,
    ):
        self._input_features = []
        self._target = None
        self._query: Query = None
        self._data_store = data_store

        self._get_feature_metadata(model=model, featureset_map=featureset_map)

    @property
    def input_features(self) -> List[types.ColumnConfig]:
        return self._input_features

    @property
    def target(self) -> types.ColumnConfig:
        return self._target

    @property
    def query(self) -> Query:
        return self._query

    @property
    def time_index(self) -> str:
        return self._query.get_time_index_name()

    @property
    def index(self) -> str:
        return self._query.get_index_name()

    @property
    def split_field(self) -> str:
        return self._query.get_split_name()

    @property
    def inferred_problem_type(self) -> str:
        """
        Gets problem type based off of outputs only
        """
        if self._target.type == types.FieldType.CATEGORICAL:
            return "multiclass_classification"
        if self._target.type == types.FieldType.BOOLEAN:
            return "binary_classification"
        if self._target.type == types.FieldType.NUMBER:
            return "regression"
        if self._target.type == types.FieldType.TEXT:
            return "text_prediction"

        raise ValueError(f"Unknown problem type for {self._target}")

    def get_data(
        self,
        local: bool = False,
        allrows: bool = False,
        database_url: str = POSTGRES_DB_URL,
    ) -> pd.DataFrame:
        """
        Returns data as pandas dataframe for this dataset
        """

        fs = get_featurestore(
            self._data_store, cached=False, cfg={"DatabaseURL": database_url}
        )
        qiter = fs.fetch_training_data(
            self._query.to_dict(),
            all_instances=allrows,
            local=local,
        )
        if local:
            return qiter

        all_dfs = []

        try:
            df = next(qiter)
            df.columns = df.columns.str.lower()
            cols = [c for c in df.columns if c.endswith("timerank")]
            if "finalrank" in df.columns:
                cols.append("finalrank")

            while df is not None:
                df.columns = df.columns.str.lower()
                if len(cols) > 0:
                    df.drop(cols, axis=1, inplace=True)
                all_dfs.append(df)
                df = next(qiter)
        except StopIteration:
            pass

        if fs:
            fs.close()

        if len(all_dfs) > 0:
            return pd.concat(all_dfs)

        return pd.DataFrame()

    def _get_feature_metadata(
        self,
        model: management_types_pb2.Model,
        featureset_map: Dict[str, management_types_pb2.FeatureSet],
    ):
        try:
            self._query = Query.form_query(
                model=model,
                metadata=True,
                all_featuresets=featureset_map,
            )
        except Exception as e:
            raise Exception(f"Unable to form query for model {model.name}: {str(e)}")

        (
            input_features_dict_lst,
            output_features_dict_lst,
        ) = self._query.get_model_version_io(include_id=True)
        if not input_features_dict_lst or not output_features_dict_lst:
            raise Exception(
                f"Input features {input_features_dict_lst} or output features {output_features_dict_lst} invalid."
            )

        if len(output_features_dict_lst) > 1:
            raise ValueError(
                f"Currently cannot handle multiple outputs: {output_features_dict_lst}"
            )

        feature_names = set()
        for feature in input_features_dict_lst:
            if feature["name"] not in feature_names:
                self._input_features.append(types.QueryFeature(**feature))
                feature_names.add(feature["name"])

        self._target = types.QueryFeature(**output_features_dict_lst[0])
        logging.info(f"Feature {output_features_dict_lst[0]}, target {self._target}")
