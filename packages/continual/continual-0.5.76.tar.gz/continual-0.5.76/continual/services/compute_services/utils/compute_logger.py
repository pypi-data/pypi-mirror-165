import sys
import logging
import os
from continual.python.blob.store import BlobStore

LOGGING_FMT = "%(asctime)s %(levelname)-4s" "[%(filename)s:%(lineno)d]  %(message)s"
LOGGING_DATEFMT = "%Y-%m-%d %H:%M:%S"


class OutputSplicer:
    """
    We set stdout and stderr to one of
    these object so that writes are duplicated to a log file as well
    as to stdout and stderr
    """

    def __init__(self, log_path: str, buffered: bool = False):
        """
        Parameters
        ----------
        log_path: str
            path to the log
        buffered: bool
            Whether to buffer output
        """
        self._log_file = open(log_path, "a+")
        self._buffered = buffered

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit 'with' context
        """
        self.close()

    def close(self):
        """
        Close file like object
        """
        self._log_file.close()

    def write(self, message):
        """
        Write to
        """
        self._log_file.write(message)
        if not self._buffered:
            self._log_file.flush()

    def flush(self):
        """
        Flush buffered output
        """
        self._log_file.flush()


class StandardOutputSplicer(OutputSplicer):
    """
    Context manager for regions where we want stdout to also go to a log file
    """

    def __enter__(self):
        """
        Enter 'with' context
        """
        self._stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit 'with' context
        """
        super().__exit__(exc_type, exc_value, traceback)
        sys.stdout = self._stdout

    def write(self, message):
        """
        Write to output
        """
        super().write(message)
        self._stdout.write(message)

    def flush(self):
        """
        Flush buffered output
        """
        super().flush()
        self._stdout.flush()


class StandardErrorSplicer(OutputSplicer):
    """
    Context manager for regions where we want stderr to also go to a log file
    """

    def __enter__(self):
        """
        Enter 'with' context
        """
        self._stderr = sys.stderr
        sys.stderr = self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit 'with' context
        """
        super().__exit__(exc_type, exc_value, traceback)
        sys.stderr = self._stderr

    def write(self, message):
        """
        Write to output
        """
        super().write(message)
        self._stderr.write(message)

    def flush(self):
        """
        Flush buffered output
        """
        super().flush()
        self._stderr.flush()


def configure_logging(master_log_path: str):
    """
    Set logging module parameters

    Parameters
    ----------
    master_log_path: str
        The master log where the output of all loggers will go
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FMT,
        datefmt=LOGGING_DATEFMT,
        filename=master_log_path,
        force=True,
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(
        logging.Formatter(fmt=LOGGING_FMT, datefmt=LOGGING_DATEFMT)
    )
    logging.root.addHandler(stdout_handler)

    logging.info(
        f"Configure training service logger to write to {os.path.abspath(master_log_path)}"
    )


def get_logger(name: str, log_file_path: str, log_level: str = "INFO"):
    """
    Return a logger with the give name that logs to a filepath

    Parameters
    ----------
    name : str
        Name of the logger
    log_file_path: str
        The path to the file that the logger will log to
    log_level: str
        The log level for the returned logger
    """

    # Create handler
    formatter = logging.Formatter(fmt=LOGGING_FMT, datefmt=LOGGING_DATEFMT)
    fh = logging.FileHandler(filename=log_file_path)
    fh.setFormatter(formatter)

    # Add handler
    logger = logging.getLogger(name)
    logger.addHandler(fh)
    logger.setLevel(log_level)

    return logger


def upload_logs(file_path: str, bucket: str, bucket_relative_path: str) -> None:
    store = BlobStore(bucket)
    store.upload_file(file_path, prefix=bucket_relative_path)
    return
