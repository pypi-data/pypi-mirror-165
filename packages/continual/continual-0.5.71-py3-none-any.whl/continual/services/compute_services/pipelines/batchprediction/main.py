import argparse
import logging
from glob import glob

from continual.python.sdk.client import Client
from continual.python.sdk.logger.logger import logger as metadata_logger
from continual.services.compute_services.pipelines.batchprediction.batch_prediction_runner import (
    BatchPredictionRunner,
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
        logging_resource=args.batch_prediction_name,
        project=get_parent(get_parent(args.batch_prediction_name)),
    )
    metadata_logger.init(
        resource=args.batch_prediction_name,
        session=args.session,
        endpoint=args.management_endpoint,
    )
    try:
        BatchPredictionRunner(
            client=client,
            batch_prediction_name=args.batch_prediction_name,
            logging_level=args.logging_level,
        ).run()
    finally:
        for log_file in glob("/app/*.log.txt"):
            client.logger.log_artifact(
                path=log_file, type="log", metadata={"name": log_file}
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
            "--batch-prediction-name",
            type=str,
            required=True,
            default="",
            help="The batch prediction to run.",
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
            default="batchprediction.master.log.txt",
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
