import socket
import sys
import logging
sys.path.append('../')
import logs.config_client_log
import logs.config_server_log

# checking which module is run (server or client)
if sys.argv[0].find('client_dist') == -1:
    logger = logging.getLogger('server_dist')
else:
    logger = logging.getLogger('client_dist')


def log(func_to_log):
    def log_saver(*args , **kwargs):
        logger.debug(f'FUnction {func_to_log.__name__} was called with params {args} , {kwargs}. Call from module'
                     f' {func_to_log.__module__}')
        ret = func_to_log(*args , **kwargs)
        return ret
    return log_saver

