import logging
import os
import sys
from typing import List

from continual.services.compute_services.utils.compute_logger import (
    get_logger,
    configure_logging,
    StandardOutputSplicer,
    StandardErrorSplicer,
)

MASTER_LOG_PATH = os.path.join(os.path.dirname(__file__), "master.test.log")


def test_configure_logger():
    cleanup()

    # First check that warnings show up and infos dont
    configure_logging(MASTER_LOG_PATH)
    logging.info("MASTER_LOG_TEST")
    logging.info("MASTER_LOG_TEST")
    logging.info("MASTER_LOG_TEST")
    logging.debug("MASTER_LOG_TEST")
    logging.debug("MASTER_LOG_TEST")

    with open(MASTER_LOG_PATH, "r") as f:
        contents = f.read()
    assert contents.count("MASTER_LOG_TEST") == 3

    # Now get a random logger from logging and perform same test
    logger = logging.getLogger("test_logger")

    logger.info("MASTER_LOG_TEST")
    logger.debug("MASTER_LOG_TEST")
    with open(MASTER_LOG_PATH, "r") as f:
        contents = f.read()
    assert contents.count("MASTER_LOG_TEST") == 4
    cleanup()


def test_redirect_std():
    cleanup()
    configure_logging(MASTER_LOG_PATH)
    with StandardOutputSplicer(MASTER_LOG_PATH), StandardErrorSplicer(MASTER_LOG_PATH):
        logging.info("LOG TEST")
        print("STDOUT TEST")
        print("STDERR TEST", file=sys.stderr)

    with open(MASTER_LOG_PATH, "r") as f:
        contents = f.read()

    assert contents.find("LOG TEST") != -1
    assert contents.find("STDOUT TEST") != -1
    assert contents.find("STDERR TEST") != -1
    cleanup()


def test_get_logger():
    log_files = [
        os.path.join(os.path.dirname(__file__), filename)
        for filename in [f"logger.{i+1}.log" for i in range(2)]
    ]
    cleanup(log_files)
    configure_logging(MASTER_LOG_PATH)
    # Create 1 logger

    logger1 = get_logger("logger1", log_files[0], log_level=logging.DEBUG)
    logger1.debug("DEBUG1")
    logger2 = get_logger("logger2", log_files[1], log_level=logging.DEBUG)
    logger2.debug("DEBUG2")

    # Check files
    with open(log_files[0], "r") as f1, open(log_files[1], "r") as f2, open(
        MASTER_LOG_PATH, "r"
    ) as fm:
        log1_contents = f1.read()
        log2_contents = f2.read()
        # Ensure master log has both
        master_file_contents = fm.read()

    assert (
        master_file_contents.find("DEBUG1") != -1
        and master_file_contents.find("DEBUG2") != -1
    )
    assert log1_contents.find("DEBUG1") != -1
    assert log2_contents.find("DEBUG2") != -1

    cleanup(log_files)


def cleanup(logs: List[str] = []):
    if os.path.exists(MASTER_LOG_PATH):
        os.remove(MASTER_LOG_PATH)
    for log in logs:
        if os.path.exists(log):
            os.remove(log)
