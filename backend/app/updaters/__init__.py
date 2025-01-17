import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="data_updates.log",
                    encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)-8s - %(message)s')