from math import isinf
import mimetypes
from typing import Optional, Any, List, Tuple

from threading import Thread

import io
import os
import time
import grpc
import json
import requests

from google.resumable_media import DataCorruption
from google.resumable_media.requests import ResumableUpload

import numpy as np
import tarfile

from continual.python.utils.client_utils import get_management_channel

from continual.python.sdk.exceptions import normalize_exceptions_for_class
from continual.python.sdk.interceptors import AuthInterceptor

from continual.rpc.management.v1 import (
    management_types_pb2,
    management_pb2_grpc,
    management_pb2,
    types as management_types_py,
)
from continual.rpc.logging.v1 import (
    logging_pb2_grpc,
    logging_pb2,
)

CHUNK_SIZE = 117440512  # 112 MB in bytes, chosen arbitrarily


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Logger:
    def __init__(
        self,
        resource: str = "",
        session: str = "",
        endpoint: str = "",
        heartbeat_interval: Optional[int] = 10,
        disable_heartbeat: Optional[bool] = False,
    ):
        self._resource = resource
        self._session = session
        self._endpoint = endpoint
        self._disable_heartbeat = disable_heartbeat
        self._heartbeat_interval = heartbeat_interval

        self.channel: grpc.Channel = None
        self.client: logging_pb2_grpc.LoggingAPIStub = None
        self.mgmt_client: management_pb2_grpc.ManagementAPIStub = None

        if self._endpoint and self._session:
            auth_interceptor = AuthInterceptor(lambda: self.session)

            self.channel = get_management_channel(self.endpoint)

            self.channel = grpc.intercept_channel(self.channel, auth_interceptor)
            self.client = normalize_exceptions_for_class(
                logging_pb2_grpc.LoggingAPIStub(self.channel)
            )
            self.mgmt_client = normalize_exceptions_for_class(
                management_pb2_grpc.ManagementAPIStub(self.channel)
            )

        self.hb_thread: HeartbeatThread = None
        self.start_heartbeat_thread()

    def __del__(self) -> None:
        if self.hb_thread:
            self.hb_thread.stop()

    def init(self, resource: str = "", session: str = "", endpoint: str = ""):
        self.set_resource(resource)
        if session:
            self.set_session(session)
        if endpoint:
            self.set_endpoint(endpoint)

    def start_heartbeat_thread(self):
        if self.hb_thread:
            self.hb_thread.stop()
        self.hb_thread = HeartbeatThread(logger=self, daemon=True)
        self.hb_thread.start()

    def start_clients(self):
        if self.endpoint and self.session:
            auth_interceptor = AuthInterceptor(lambda: self.session)

            self.channel = get_management_channel(self.endpoint)

            self.channel = grpc.intercept_channel(self.channel, auth_interceptor)
            self.client = normalize_exceptions_for_class(
                logging_pb2_grpc.LoggingAPIStub(self.channel)
            )
            self.mgmt_client = normalize_exceptions_for_class(
                management_pb2_grpc.ManagementAPIStub(self.channel)
            )

    @property
    def resource(self) -> str:
        return self._resource

    def set_resource(self, r: str):
        if (not is_model_version(r)) and (not is_batch_prediction(r)):
            raise ValueError(
                f"Unrecognized resource name passed into logger: {r}. Must match name pattern of either ModelVersion or BatchPrediction."
            )
        restart_hb = r != self._resource
        self._resource = r
        if restart_hb:
            self.start_heartbeat_thread()

    @property
    def is_model_version(self) -> bool:
        return is_model_version(self.resource)

    @property
    def is_batch_prediction(self) -> bool:
        return is_batch_prediction(self.resource)

    @property
    def session(self) -> str:
        return self._session

    def set_session(self, s: str):
        if not is_session(s):
            raise ValueError(f"Invalid session token passed into logger: {s}")
        self._session = s
        self.start_clients()

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def set_endpoint(self, e: str):
        if e not in (
            "https://api.continual.ai",
            "https://api-benchmark.continual.ai",
            "http://127.0.0.1",
            "http://localhost",
            "http://host.docker.internal",
            "http://cluster",
        ):
            raise ValueError(f"Unsupported endpoint passed into logger: {e}")
        self._endpoint = e
        self.start_clients()

    @property
    def disable_heartbeat(self) -> bool:
        return self._disable_heartbeat

    def set_disable_heartbeat(self, disable: bool):
        self._disable_heartbeat = disable

    @property
    def heartbeat_interval(self) -> int:
        return self._heartbeat_interval

    def set_heartbeat_interval(self, interval: int):
        if interval < 0 or isinf(interval):
            raise ValueError(
                f"Invalid heartbeat interval passed into logger: {interval}"
            )
        self._heartbeat_interval = interval

    def log_heartbeat(self):
        if not self.client or not self.resource:
            return
        req = logging_pb2.LogHeartbeatRequest(resource=self.resource)
        self.client.LogHeartbeat(req)
        # print(
        #     f"[HEARTBEAT] Resource=({self.resource}) at {datetime.utcnow().isoformat()}"
        # )

    def log_state(self, state: management_types_py.ModelVersionState):
        if not self.client or not self.is_model_version:
            print(f"State: {state}")
            return

        req = logging_pb2.LogModelVersionRequest(
            model_version=management_types_pb2.ModelVersion(
                name=self.resource, state=state.to_proto()
            ),
            update_paths=["state"],
        )
        res = self.client.LogModelVersion(req)
        print(f"log_state: {res}")

    def log_field(self, field_name: str, value: Any):
        if not self.client:
            raise Exception(f"Client not set in logger.")

        resource_args = {"name": self.resource, field_name: value}

        if self.is_model_version:
            req = logging_pb2.LogModelVersionRequest(
                model_version=management_types_pb2.ModelVersion(**resource_args),
                update_paths=[field_name],
            )
            res = self.client.LogModelVersion(req)
        else:
            req = logging_pb2.LogBatchPredictionRequest(
                batch_prediction=management_types_pb2.BatchPrediction(**resource_args),
                update_paths=[field_name],
            )
            res = self.client.LogBatchPrediction(req)
        print(f"log_field: {field_name} with {value} on {self.resource} : {res}")

    def log_predict_state(self, state: management_types_py.BatchPredictionState):
        if not self.client or not self.is_batch_prediction:
            print(f"State: {state}")
            return

        req = logging_pb2.LogBatchPredictionRequest(
            batch_prediction=management_types_pb2.BatchPrediction(
                name=self.resource, state=state.to_proto()
            ),
            update_paths=["state"],
        )
        res = self.client.LogBatchPrediction(req)
        print(f"log_predict_state: {res}")

    def get_artifact(self, name: str) -> management_types_pb2.Artifact:
        if not self.client:
            print(f"Cannot fetch artifact without client")
            return

        req = logging_pb2.GetArtifactRequest(name=name)
        res = self.client.GetArtifact(req)
        return res

    def delete_artifact(self, name: str):
        if not self.client:
            print(f"Cannot delete artifact without client")
            return

        req = logging_pb2.DeleteArtifactRequest(name=name)
        self.client.DeleteArtifact(req)

    def get_model_artifact(
        self,
        model_version: str = "",
        download: bool = False,
        download_dir: str = "./artifacts",
    ) -> Tuple[management_types_pb2.Artifact, str]:
        if not self.client:
            print(f"Cannot fetch artifact without client")
            return

        req = management_pb2.GetModelVersionRequest(name=model_version or self.resource)
        res = self.mgmt_client.GetModelVersion(req)
        print(f"get_model_artifact res: {res}")
        if not res.model_artifact:
            raise ValueError(
                f"Model version ({model_version}) does not have a model artifact."
            )

        artifact = self.get_artifact(res.model_artifact)
        downloaded_to = ""
        if download:
            if not artifact.url:
                raise ValueError(
                    f"Artifact cannot be downloaded - no URL was found: {artifact.url}"
                )
            try:
                res = requests.get(artifact.url, stream=True)
                with tarfile.open(fileobj=res.raw, mode="r") as f:
                    f.extractall(download_dir)

                root_dir = os.path.basename(artifact.path or "").split(".")[0]
                downloaded_to = os.path.join(download_dir, root_dir)
            except:
                res = requests.get(artifact.url)
                downloaded_to = os.path.join(
                    download_dir,
                    os.path.basename(artifact.path or artifact.name.split("/")[-1]),
                )
                with open(downloaded_to, "wb") as f:
                    f.write(res.content)
        return artifact, downloaded_to

    def log_model_artifact(self, path: str, metadata: dict = None) -> str:
        if not self.is_model_version:
            print(f"Cannot log model artifact to a BatchPrediction.")
            return

        artifact_name = self.log_artifact(path=path, type="model", metadata=metadata)
        req = logging_pb2.LogModelVersionRequest(
            model_version=management_types_pb2.ModelVersion(
                name=self.resource,
                model_artifact=artifact_name,
            ),
            update_paths=["model_artifact"],
        )
        res = self.client.LogModelVersion(req)
        print(f"log_model_artifact: {res}")
        return artifact_name

    def log_artifacts(
        self, paths: List[str], type: str = "", metadata: dict = None
    ) -> List[str]:
        artifact_names = []
        for path in paths:
            try:
                name = self.log_artifact(path=path, type=type, metadata=metadata)
                artifact_names.append(name)
            except:
                artifact_names.append("")
        return artifact_names

    def log_artifact(self, path: str, type: str = "", metadata: dict = None) -> str:
        if not metadata:
            metadata = {}

        if not self.client:
            print(f"Artifact: path={path}, type={type} metadata={metadata}")
            return

        if not os.path.exists(path):
            raise ValueError(
                f"Invalid file path provided. Path ({path}) does not exist."
            )

        artifact_name = ""

        try:
            file_to_upload = path
            if os.path.isdir(path):
                tarfile_name = os.path.basename(path) + ".tar.gz"
                with tarfile.open(tarfile_name, "w:gz") as tar:
                    tar.add(
                        path,
                        recursive=True,
                        arcname=os.path.basename(tarfile_name).split(".")[0],
                    )
                file_to_upload = tarfile_name

            mime_type, _ = mimetypes.guess_type(file_to_upload)

            payload = ""
            with open(file_to_upload, "rb") as f:
                payload = f.read()

            total_bytes = len(payload)
            exceeds_chunk_size = total_bytes >= CHUNK_SIZE

            req = logging_pb2.GenerateArtifactUploadURLRequest(
                resource=self.resource,
                path=path,
                type=type,
                mime_type=mime_type or "",
                metadata=json.dumps(metadata or dict()),
                resumable=exceeds_chunk_size,
            )
            res = self.client.GenerateArtifactUploadURL(req)

            upload_url = res.url
            artifact_name = res.artifact.name

            headers = dict()
            if mime_type:
                headers["Content-Type"] = mime_type

            if exceeds_chunk_size:
                transport = requests.Session()
                metadata = dict(name=artifact_name, file=path)

                stream = io.BytesIO(payload)

                upload = ResumableUpload(upload_url, CHUNK_SIZE)
                upload._resumable_url = upload_url
                upload._total_bytes = total_bytes
                upload._stream = stream

                while not upload.finished:
                    try:
                        print("Writing chunk ... ")
                        response = upload.transmit_next_chunk(transport, timeout=60)
                        print(f"Chunk response: {response}")
                    except DataCorruption:
                        raise
            else:
                upload_res = requests.put(
                    upload_url, data=payload, headers={"Content-Type": mime_type}
                )
                upload_res.raise_for_status()

            return artifact_name
        except:
            if artifact_name:
                req = logging_pb2.DeleteArtifactRequest(name=artifact_name)
                res = self.client.DeleteArtifact(req)
            raise

    def log_data_checks(self, data_checks: management_types_pb2.DataChecks):
        if not self.client:
            print(f"Data Checks: {data_checks}")
            return

        req = logging_pb2.LogDataChecksRequest(
            resource=self.resource, data_checks=data_checks
        )
        res = self.client.LogDataChecks(req)
        print(f"log_data_checks: {res}")

    def log_prediction_stats(self, prediction_stats: management_types_pb2.DatasetStats):
        if not self.client or not self.is_batch_prediction:
            print(f"Prediction Stats: {prediction_stats}")
            return

        req = logging_pb2.LogPredictionStatsRequest(
            batch_prediction=self.resource, prediction_stats=prediction_stats
        )
        res = self.client.LogPredictionStats(req)
        print(f"log_prediction_stats: {res}")

    def log_eval_model_version_metrics(
        self,
        eval_model_version_metrics: management_types_pb2.EvaluationModelVersionMetrics,
    ):
        if not self.client:
            print(f"Dataset Stats: {eval_model_version_metrics}")
            return

        req = logging_pb2.LogEvaluationModelMetricsRequest(
            model_version=self.resource,
            evaluation_model_version_metrics=eval_model_version_metrics,
        )
        res = self.client.LogEvaluationModelMetrics(req)
        print(f"log_eval_model_version_metrics: {res}")

    def log_dataset_stats(self, dataset_stats: management_types_pb2.DatasetStats):
        if not self.client:
            print(f"Dataset Stats: {dataset_stats}")
            return

        req = logging_pb2.LogDatasetStatsRequest(
            resource=self.resource, dataset_stats=dataset_stats
        )
        res = self.client.LogDatasetStats(req)
        print(f"log_dataset_stats: {res}")

    def log_metrics(self, metrics: List[management_types_py.TrainingMetrics]):
        if not self.client:
            print(f"Metrics: {metrics}")
            return

        req = logging_pb2.LogMetricsRequest(
            model_version=self.resource,
            metrics=list(map(lambda m: m.to_proto(), metrics)),
        )
        res = self.client.LogMetrics(req)
        print(f"log_metrics: {res}")

    def log_experiment(self, experiment: management_types_py.Experiment):
        self.log_experiments(experiments=[experiment])

    def log_experiments(self, experiments: List[management_types_py.Experiment]):
        if not self.client:
            print(f"Experiments: {experiments}")
            return
        req = logging_pb2.LogExperimentsRequest(
            model_version=self.resource,
            experiments=list(map(lambda e: e.to_proto(), experiments)),
        )
        res = self.client.LogExperiments(req)
        print(f"log_experiments: {res}")

    def log_metadata(self, metadata: dict = None):
        if not self.client:
            print(f"Metadata: {metadata}")
            return
        self.log_field("metadata", json.dumps(metadata, cls=NpEncoder))


class HeartbeatThread(Thread):
    def __init__(self, logger: Logger, *args, **kwargs) -> None:
        Thread.__init__(self, *args, **kwargs)
        self.logger = logger
        self.running = True
        self.should_stop = False

    def stop(self):
        self.should_stop = True
        self.running = False

    def run(self) -> None:
        while True:
            if self.should_stop:
                break
            self.logger.log_heartbeat()
            time.sleep(self.logger.heartbeat_interval or 5)


def is_model_version(name: str) -> bool:
    name_split = name.split("/")
    if (
        len(name_split) != 6
        or name_split[0] != "projects"
        or name_split[2] != "models"
        or name_split[4] != "versions"
    ):
        return False
    return True


def is_batch_prediction(name: str) -> bool:
    name_split = name.split("/")
    if (
        len(name_split) != 6
        or name_split[0] != "projects"
        or name_split[2] != "models"
        or name_split[4] != "batchPredictions"
    ):
        return False
    return True


def is_session(name: str) -> bool:
    name_split = name.split("/")
    if len(name_split) != 2 or name_split[0] != "sessions":
        return False
    return True


logger = Logger()
