import sys
import logging
import project_logs.config.config_server
import project_logs.config.config_client
import inspect


if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        result = func_to_log(*args, **kwargs)
        logger.debug(f'Function {func_to_log.__name__} was called with {args}, {kwargs} parameters.'
                     f'Module\'s name: {func_to_log.__module__}.The call is from function {inspect.stack()[1][3]}',
                     stacklevel=2)
        return result
    return log_saver


class Log:
    def __call__(self, func_to_log):
        def log_saver(*args, **kwargs):
            result = func_to_log(*args, **kwargs)
            logger.debug(f'Function {func_to_log.__name__} was called with {args}, {kwargs} parameters.'
                         f'Module\'s name: {func_to_log.__module__}.The call is from function {inspect.stack()[1][3]}',
                         stacklevel=2)
            return result
        return log_saver
