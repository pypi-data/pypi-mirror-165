import json
import tempfile
import traceback
from continual.python.sdk.datasets import Dataset


from continual.python.sdk.extensions.models.base_model_pipeline import BaseModelPipeline
from continual.python.sdk.client import Client
from continual.services.compute_services.utils.compute_logger import (
    get_logger,
)
from continual.services.compute_services.pipelines.pipeline_utils import get_pipeline

LOG_FILE_NAME = "training.runner.log.txt"


class TrainingPipelineRunner:
    def __init__(
        self,
        client: Client,
        model_version_name: str,
        logging_level: str = "INFO",
    ):

        self.client = client
        self.config = client.model_versions.get_train_config(
            model_version_name=model_version_name
        )
        self.logging_level = logging_level

        # Construct utils
        self.logger = get_logger(__name__, LOG_FILE_NAME, logging_level)
        self.logger.info(f"Starting TrainingPipeline runner for {model_version_name} ")

        # Construct arguments
        self.model_version = self.config.model_version
        self.model = self.config.model.to_proto()
        self.featureset_map = {}
        for fs in self.config.feature_sets:
            self.logger.info(f"feature set joined in: {fs}")
            self.featureset_map[fs.name] = fs.to_proto()

        if not self.config.feature_sets:
            self.logger.info(
                f"No feature sets found to join in for model version: {model_version_name}."
            )

        self.data_store = self.config.data_store.to_proto()
        self.tag = self.config.tag
        self.evaluation_model_version = self.config.evaluation_model_version
        self.evaluation_model_signature = self.config.evaluation_model_signature
        self.output_dir = tempfile.mkdtemp()
        self.fit_config = {}
        if self.model_version.fit_config != "":
            self.fit_config = json.loads(self.model_version.fit_config)

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
            train_data = Dataset(
                model=self.model,
                featureset_map=self.featureset_map,
                data_store=self.data_store,
            )
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors("Error constructing dataset", e, stack_trace)
            raise

        # Get and init pipeline
        try:
            pipeline: BaseModelPipeline = get_pipeline(
                client=self.client, pipeline_id=self.model.schema.pipeline.name
            )()
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors(f"Exception getting pipeline", e, stack_trace)
            raise

        # Training
        self._train_args = dict(
            client=self.client,
            model_version_name=self.model_version.name,
            train_data=train_data,
            output_dir=self.output_dir,
            fit_config=self.fit_config,
            evaluation_model_version_name=self.evaluation_model_version,
            evaluation_model_signature=self.evaluation_model_signature,
            model=self.model,
            tag=self.tag,
            data_store=self.data_store,
            log_level=self.logging_level,
        )

        try:
            pipeline.train(**self._train_args)
        except Exception as e:
            stack_trace = traceback.format_exc()
            self._set_errors(f"Exception during train", e, stack_trace)
            raise

        # Successful train and promote
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
