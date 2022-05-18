# import logging
import logging.handlers
import os
import sys

from common.settings import LOGGING_LEVEL

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs/server.log')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)

file_handler = logging.handlers.TimedRotatingFileHandler(PATH, when='D', encoding='utf-8', interval=1)
file_handler.setFormatter(formatter)

logger = logging.getLogger('server')
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.debug('debug server test')
    logger.info('info server test')
    logger.warning('warning server test')
    logger.error('error server test')
    logger.critical('critical server test')
