from abc import ABC, abstractclassmethod
import pandas as pd

from continual.python.utils.utils import parse_model_name
from .featurestore import get_featurestore

from jinja2 import Template
from datetime import datetime
from urllib.parse import urlparse, parse_qs

PREDICTION_TABLE_NAME = "predictions"

# running into "Compilation memory exhausted" errors so setting lower
# TODO: optimize this size
WRITE_CHUNK_SIZE = 1000

# Based on Snowflake limit of 1M
MAX_QUERY_LEN = 900 * 1024 * 1024

insert_template = Template(
    """INSERT INTO  {{param.project}}.{{param.table_name}} ({% for r in param.insert_list %}{%if loop.index0 != 0%},{% endif %}{{r}}{% endfor %})
        SELECT {% for r in param.columns %}{%if loop.index0 != 0%},{% endif %}{{r}}{% endfor %} 
        FROM {{param.project}}.{{param.temp_table}}"""
)


def parse_connection_url(connection_url):
    upass = urlparse(connection_url)
    qpass = parse_qs(upass.query)
    upass_splits = upass.netloc.split("@")
    username = upass_splits[0].split(":")[0]
    password = upass_splits[0].split(":")[1]
    account = upass_splits[1]
    database = upass.path.strip("/")
    warehouse = qpass.get("warehouse", None)
    if warehouse is not None:
        warehouse = warehouse[0]
    role = qpass.get("role", None)
    if role is not None:
        role = role[0]

    return account, username, password, database, warehouse, role


def chunk_it(start, end, step=WRITE_CHUNK_SIZE):
    if start >= end:
        return None

    if start + step > end:
        return (start, end)

    return (start, start + step)


class PredictionStore(ABC):
    def __init__(self, datastore):
        # db_url = "postgresql://continual:continual@localhost:5432/continual"
        self.datastore = datastore
        self.engine = None
        self.connection = None

    @staticmethod
    def getStore(
        datastore,
        cfg: dict = None,
    ):
        if datastore is None:
            return None

        return get_featurestore(data_store=datastore, cfg=cfg)

    def parse_batchPrediction_job_name(self, name):
        splits = name.split("/")
        project_name = "/".join(splits[:2])
        model_name = "/".join(splits[:4])
        return project_name, model_name

    def get_model_prediction_table_name(self, model):
        project_id, model_id = parse_model_name(model.name)
        project_id = project_id.replace("@", "_")
        return project_id, "model_{}_predictions_history".format(model_id)

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

        all_times = list(df.select_dtypes(include=["datetimetz", "datetime64"]).columns)
        for t in all_times:
            df[t] = df[t].apply(lambda x: x.isoformat())

        df["batch_prediction"] = name
        df["model_version"] = model_version

        df = df.where(pd.notnull(df), None)
        return df

    @abstractclassmethod
    def write_prediction(
        self,
        df: pd.DataFrame,
        id_column_name: str,
        ts_column_name: str,
        model_query: any,
        output_name: str,
        job_name: str,
        job_start_time: datetime,
        model: any,
        model_version: str,
        time_index_dtype,
    ):
        pass

    def close(self):
        pass
