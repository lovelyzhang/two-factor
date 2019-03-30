import logging
import logging.handlers
import sys

format_string = '[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)s]:%(message)s'
datefmt_string = '%Y-%m-%d %H:%M:%S'
LEVEL_DICT = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG
}


def getlogger(name, level="INFO",
              filename=None, when=None, interval=1, backupCount=10):
    """
        Default to console output.
        When set file and when, using TimedRotatingFileHandler
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
    """
    logger = logging.getLogger(name)
    if filename:
        if when:
            handler = logging.handlers.TimedRotatingFileHandler(filename,
                                                                when=when,
                                                                interval=interval,
                                                                backupCount=backupCount)
        else:
            handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(format_string, datefmt=datefmt_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LEVEL_DICT.get(level))
    return logger


AUTH_LOGGER = getlogger("auth_logger")
