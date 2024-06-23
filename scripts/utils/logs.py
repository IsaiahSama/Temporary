"""This file will be responsible for handling the logging of the script."""
import logging
from .enums import RestaurantNames
from datetime import datetime
from .custom_exceptions import *
import os

base_dir = os.path.dirname(__file__)
logs_dir = os.path.join(base_dir, "..", "..", "documents", "Logs")

os.makedirs(logs_dir, exist_ok=True)

LOG_FILE = os.path.join(logs_dir, "logs.txt")

logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger("root")

class Logger:
    """
    This class will be responsible for handling the logging of the script."""
    
    @staticmethod
    def log(message: str):
        print(message)
        logger.info(message)

    @staticmethod
    def error(message: str):
        print(message)
        logger.error(message)

    @staticmethod
    def warning(message: str):
        print(message)
        logger.warning(message)

    @staticmethod
    def clear():
        with open(LOG_FILE, 'w') as f:
            f.write("")

        Logger.warning("Cleared log file")
