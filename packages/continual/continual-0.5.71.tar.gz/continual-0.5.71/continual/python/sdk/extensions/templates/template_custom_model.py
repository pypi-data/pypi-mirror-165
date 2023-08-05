from typing import Any
import shortuuid

from continual.python.sdk.extensions.models.base_model_pipeline import BaseModelPipeline
from continual.python.sdk.datasets import Dataset
from continual.python.sdk.client import Client
from continual.rpc.management.v1 import types, management_types_pb2
from continual.python.utils.utils import get_experiment_name, get_current_time


class MyModelPipeline(BaseModelPipeline):
    def train(
        self,
        client: Client,
        model_version_name: str,
        train_data: Dataset,
        output_dir: str,
        fit_config: dict,
        evaluation_model_version_name: str,
        evaluation_model_signature: str,
        model,
        tag,
        data_store,
        log_level: str,
        **kwargs: dict,
    ):
        """
        Train model, log a model
        version state, and a model artifact
        """
        experiment_name = get_experiment_name(
            model_version_name=model_version_name,
            experiment_id=shortuuid.uuid().lower(),
        )
        # Log an experiment
        client.logger.log_field(field_name="start_time", value=get_current_time())
        client.logger.log_experiment(
            types.Experiment(
                name=experiment_name,
                type="TemplateAlgorithm",
                performance_metric="rmse",
                performance_metric_val=40.0,
                state=types.ExperimentState.SUCCEEDED,
                start_time=get_current_time().ToDatetime(),
                finish_time=get_current_time().ToDatetime(),
            )
        )

        # Register winning experiment
        client.logger.log_field(
            "experiment",
            experiment_name,
        )
        client.logger.log_field("performance_metric_val", 40.0)

        # RegisterEvaluation state
        client.logger.log_eval_model_version_metrics(
            types.EvaluationModelVersionMetrics(
                state=types.EvaluationModelVersionMetricsState.NO_DEPLOYED_VERSION
            ).to_proto(),
        )
        client.logger.log_state(state=types.ModelVersionState.SUCCEEDED)

    def predict(
        self,
        client: Client,
        model_version_name: str,
        batch_prediction_name: str,
        predict_data: Dataset,
        model,
        data_store,
        model_version_signature: Any,
        disable_feature_timestamp_generation: bool,
        log_level: str,
        **kwargs: dict,
    ):
        """
        Use a trained model to make batch predictions
        on some given data. Log the batch prediction
        state and write the batch predictions to the
        data store
        """

        client.logger.log_field(field_name="start_time", value=get_current_time())
        ds_stats = management_types_pb2.DatasetStats(
            resource_name=batch_prediction_name,
            profile_time=get_current_time(),
            dataset_stats=[
                management_types_pb2.DatasetStatsEntry(**{}),
            ],
        )
        client.logger.log_dataset_stats(ds_stats)
        client.logger.log_predict_state(state=types.BatchPredictionState.SUCCEEDED)
