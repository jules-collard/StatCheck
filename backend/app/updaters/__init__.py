import logging
from sqlalchemy.exc import IntegrityError
import os

log_path = os.path.join(os.path.dirname(__file__), "data_updates.log")

logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_path,
                    encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)-8s - %(message)s')

def log_error(e: IntegrityError):
    logger.debug(e.statement)
    logger.debug(e.orig)