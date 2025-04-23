import logging
from logging.handlers import RotatingFileHandler
import os
import sys


def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Get a configured logger with the specified name.
    """
    # Constants
    LOG_FILE = "logs/app.log"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the log level
    logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if LOG_FILE:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_FILE_SIZE, backupCount=BACKUP_COUNT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
