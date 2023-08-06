import traceback


from continual.python.sdk.client import Client
from continual.python.sdk.datasets import Dataset
from continual.python.sdk.extensions.models.base_model_pipeline import BaseModelPipeline
from continual.services.compute_services.pipelines.pipeline_utils import get_pipeline
from continual.services.compute_services.utils.compute_logger import (
    get_logger,
)

LOG_FILE_NAME = "batchprediction.runner.log.txt"


class BatchPredictionRunner:
    def __init__(
        self, client: Client, batch_prediction_name: str, logging_level: str = "INFO"
    ):

        self.client = client
        self.config = client.batch_prediction_jobs.get_batch_prediction_config(
            batch_prediction_name=batch_prediction_name
        )
        self.logging_level = logging_level

        # Extract config parameters
        self.batch_prediction_name = batch_prediction_name
        self.model_version_name = self.config.model_version
        self.model = self.config.model.to_proto()
        self.model_schema = self.model.schema
        self.data_store = self.config.data_store.to_proto()
        self.incremental = self.config.incremental
        self.model_version_signature = self.config.model_version_signature
        if (
            self.model_schema.train
            and self.model_schema.train.disable_feature_timestamp_generation
        ):
            self.disable_feature_timestamp_generation = (
                self.model_schema.train.disable_feature_timestamp_generation
            )
        else:
            self.disable_feature_timestamp_generation = False

        self.logger = get_logger(__name__, LOG_FILE_NAME, self.logging_level)

        self.featureset_map = {}
        for fs in self.config.feature_sets:
            self.logger.info(f"joining in feature set: {fs}")
            self.featureset_map[fs.name] = fs.to_proto()

        if not self.config.feature_sets:
            self.logger.info(
                f"No feature sets to join in for batch prediction: {batch_prediction_name}"
            )

    def run(self):
        """
        Constructs pipeline
        Constructs train args
        Constructs promote args
        Runs Train
        Runs Promote
        Logs errors
        """
        # Collect data
        try:
            predict_data = Dataset(
                model=self.model,
                featureset_map=self.featureset_map,
                data_store=self.data_store,
            )
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors("Error getting data", e, stack_trace)
            raise

        try:
            pipeline: BaseModelPipeline = get_pipeline(
                client=self.client, pipeline_id=self.model.schema.pipeline.name
            )()
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors(f"Exception getting pipeline", e, stack_trace)
            raise

        # Do batch prediction
        self._batch_predict_args = dict(
            client=self.client,
            model_version_name=self.model_version_name,
            batch_prediction_name=self.batch_prediction_name,
            predict_data=predict_data,
            model=self.model,
            data_store=self.data_store,
            model_version_signature=self.model_version_signature,
            disable_feature_timestamp_generation=self.disable_feature_timestamp_generation,
            log_level=self.logging_level,
        )

        try:
            pipeline.predict(**self._batch_predict_args)
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors(f"Exception during batchpredict", e, stack_trace)
            raise

        # Successful predict
        self._set_errors(clear=True)

    def _set_errors(
        self, message=None, e: Exception = None, stack_trace: str = None, clear=False
    ):
        """
        Make sure errors are recorded in the logs as well as the
        model version

        Parameters
        ---------
        message: str
            Description of what pipeline step the exception occured in
        e: Exception
            The exception itself
        """

        if clear:
            self.client.logger.log_field("error_message", "")
            self.client.logger.log_field("stack_trace", "")
        else:
            error_message = f"{message}:\n {e}"
            self.logger.error(f"{message}:\n {e} : {stack_trace}")
            self.client.logger.log_field("error_message", error_message)
            self.client.logger.log_field("stack_trace", stack_trace)
