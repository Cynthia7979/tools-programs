import logging
import os
from time import strftime


if os.path.exists('./log.debug'):
    LOG_LEVEL = open('./log.debug')
else:
    LOG_LEVEL = logging.DEBUG


def log_init(fname):
    global file_handler, formatter, self_logger

    log_directory = os.path.join(os.getcwd(), 'logs/')
    if not fname:
        fname = 'tool-program'
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    file_handler = logging.FileHandler(strftime('{}/{}_log_%y-%m-%d_%H-%M-%S.log'.format(log_directory, fname)))
    file_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('[%(asctime)s] %(name)s (%(levelname)s): %(message)s')
    file_handler.setFormatter(formatter)

    public_logger = logging.getLogger('Tool-Program.{}'.format(fname))
    public_logger.addHandler(file_handler)
    self_logger = logging.getLogger('Tool-Program.log')
    self_logger.addHandler(file_handler)
    return public_logger


def get_level():
    d = {'debug': logging.DEBUG,
         'info': logging.INFO,
         'warning': logging.WARNING,
         'error': logging.ERROR,
         'critical': logging.CRITICAL}
    try:
        f = open('debug')
        t = f.read()
    except FileNotFoundError:
        t = 'debug'
    if t in d.keys(): return d[t]
    else: return logging.INFO


# Logged decorator
def logged(cls, fname):
    class_name = cls.__name__
    logger = logging.getLogger('Tool-Program.{}.{}'.format(fname, class_name))
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.propagate = False
    setattr(cls, 'logger', logger)
    return cls
