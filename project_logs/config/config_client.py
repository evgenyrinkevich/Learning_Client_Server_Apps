import logging
import os
import sys

from common.settings import LOGGING_LEVEL

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs/client.log')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)

file_handler = logging.FileHandler(PATH, encoding='utf-8')
file_handler.setFormatter(formatter)

logger = logging.getLogger('client')
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.debug('debug test')
    logger.info('info test')
    logger.warning('warning test')
    logger.error('error test')
    logger.critical('critical test')
