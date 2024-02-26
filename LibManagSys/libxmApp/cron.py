import logging


logger = logging.getLogger(__name__)


def print_hello():
    print("Hello")
    logger.info("Cron Job was Called")