"""
Debug logging utility
"""

import os
import logging
from logging.handlers import RotatingFileHandler

fh = RotatingFileHandler(
    os.path.join(os.path.dirname(__file__), 'debug.log'),
    maxBytes=1024 * 1024,
    backupCount=0
)
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s(%(levelno)s) - %(message)s'))

logger = logging.getLogger('priority-reorder')
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

def log(level: int, message: str) -> None:
    global logger
    if level == DEBUG:
        logger.debug(message)
    elif level == INFO:
        logger.info(message)
    elif level == WARNING:
        logger.warning(message)
    elif level == ERROR:
        logger.error(message)
    elif level == CRITICAL:
        logger.critical(message)

