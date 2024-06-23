"""This file will be responsible for handling the logging of the script."""
import logging
from .enums import RestaurantNames
from datetime import datetime
from .custom_exceptions import *
import os


LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "documents", "Logs", "logs.txt")

logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger("4am")

class Logger:
    
    @staticmethod
    def log(message: str):
        logger.info(message)

    @staticmethod
    def error(message: str):
        logger.error(message)

    @staticmethod
    def warning(message: str):
        logger.warning(message)

    @staticmethod
    def clear():
        with open(LOG_FILE, 'w') as f:
            f.write("")

        Logger.warning("Cleared log file")
