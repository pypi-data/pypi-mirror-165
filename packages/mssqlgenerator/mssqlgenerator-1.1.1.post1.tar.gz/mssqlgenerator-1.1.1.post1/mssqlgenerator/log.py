"""
Logging-related sruff.
"""

import os
from pathlib import Path
import logging


LOG_FILE = 'logs/sql_generator.log'
# DEFAULT: don't write to terminal
PRINT_TERMINAL = False
# DEFAULT: always write to log
SKIP_LOG_WRITE = False


logger = logging.getLogger(__name__)

def init_logger(log_file=LOG_FILE):
    # generate log file path if does not exist
    log_file_directory = Path(log_file).parent.resolve()
    if log_file_directory and not os.path.exists(log_file_directory):
        os.makedirs(log_file_directory)
    # set log level
    logger.setLevel(logging.INFO)
    # log format
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s', '%Y-%m-%d %H:%M:%S')    
    # log file handler
    filehandler = logging.FileHandler(log_file, 'a')
    filehandler.setFormatter(formatter)
    # remove previous log file handlers
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    # set log file handler
    logger.addHandler(filehandler)

init_logger()

def sqllogger(*string):
    if PRINT_TERMINAL:
        print(*string) 
    if not SKIP_LOG_WRITE:
        logger.info(*string)

def print_to_terminal_ON():
    global PRINT_TERMINAL
    PRINT_TERMINAL = True

def print_to_terminal_OFF():
    global PRINT_TERMINAL
    PRINT_TERMINAL = False

def write_to_log_ON():
    global SKIP_LOG_WRITE
    SKIP_LOG_WRITE = False

def write_to_log_OFF():
    global SKIP_LOG_WRITE
    SKIP_LOG_WRITE = True
