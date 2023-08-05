# logger.py

import logging
from logging import Logger
from typing import Union
import os

default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
base_name = "main"


class CDFLogger:
    """Class containing loggers for different purposes that are used to print logs to the console during deployment"""

    def __init__(self, base_name: str):
        """Class constructor that sets the base name for the logger

        Args:
            base_name (str): base name for the logger
        """
        self.base_name = base_name

    def debug(self, log: str):
        """Debug log

        Args:
            log (str): debug log message
        """
        print(f"{self.base_name} - DEBUG - {log}")

    def info(self, log: str):
        """Info log

        Args:
            log (str): info log message
        """
        print(f"{self.base_name} - INFO - {log}")

    def warning(self, log: str):
        """Warning log

        Args:
            log (str): warning log message
        """
        print(f"{self.base_name} - WARNING - {log}")

    def error(self, log: str):
        """Error log

        Args:
            log (str): error log message
        """
        print(f"{self.base_name} - ERROR - {log}")

    def critical(self, log: str):
        """Critical log

        Args:
            log (str): critical log message
        """
        print(f"{self.base_name} - CRITICAL - {log}")


def get_logger(
    name: str = base_name, format: str = default_format
) -> Union[CDFLogger, Logger]:
    """
    Set up a stream logger

    Args:
        name (str): name of the logger. Defaults to the global base_name variable
        format (str): format of the logger. Defaults to the global default_format variable

    Returns:
        (Union[CDFLogger, Logger]): logger object
    """

    # can't use config module for this one or there would be circular imports
    if os.getenv("PLATFORM") == "cdf":
        return CDFLogger(base_name)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    stream_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(stream_handler)
    return logger
