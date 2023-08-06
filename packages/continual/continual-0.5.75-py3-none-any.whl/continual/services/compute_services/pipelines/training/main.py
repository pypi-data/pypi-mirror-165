import argparse
import logging
from glob import glob

from continual.python.sdk.client import Client
from continual.python.sdk.logger.logger import logger as metadata_logger
from continual.services.compute_services.pipelines.training.training_runner import (
    TrainingPipelineRunner,
)
from continual.services.compute_services.utils.compute_logger import (
    configure_logging,
    StandardOutputSplicer,
    StandardErrorSplicer,
)
from continual.python.utils.utils import get_parent


def main(args):
    client = Client(
        api_key=args.session,
        endpoint=args.management_endpoint,
        logging_resource=args.model_version,
        project=get_parent(get_parent(args.model_version)),
    )
    metadata_logger.init(
        resource=args.model_version,
        session=args.session,
        endpoint=args.management_endpoint,
    )
    try:
        TrainingPipelineRunner(
            client=client,
            model_version_name=args.model_version,
            logging_level=args.logging_level,
        ).run()
    finally:
        for log_file in glob("/app/*.log.txt"):
            client.logger.log_artifact(
                path=log_file, type="log", metadata=dict(name=log_file)
            )


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--logging-level",
            type=str,
            required=False,
            default="INFO",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"],
            help="Logging levels (equivalent to python logging module levels)",
        )
        parser.add_argument(
            "--model_version",
            type=str,
            required=True,
            default="",
            help="The model version name to be trained.",
        )
        parser.add_argument(
            "--session",
            type=str,
            required=True,
            default="",
            help="The authenticared session to use for API calls",
        )
        parser.add_argument(
            "--management-endpoint",
            type=str,
            required=False,
            default="https://api.continual.ai",
            help="Address of the Management service.",
        )
        parser.add_argument(
            "--service-log-path",
            type=str,
            required=False,
            default="training.master.log.txt",
            help="Path to the file where all records from training service are logged.",
        )
        in_args = parser.parse_args()
        configure_logging(
            master_log_path=in_args.service_log_path,
        )
        with StandardOutputSplicer(
            log_path=in_args.service_log_path
        ), StandardErrorSplicer(log_path=in_args.service_log_path):
            main(in_args)
    except Exception as e:
        logging.error("Exception in main program: [{}]".format(e))
        raise e
