import logging
import os
from time import strftime


LOG_LEVEL = logging.DEBUG


def log_init(fname):
    global file_handler, stream_handler, self_logger

    log_directory = os.path.join(os.getcwd(), 'logs/')
    if not fname:
        fname = 'tool-program'
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    file_handler = logging.FileHandler(strftime('{}/{}_log_%y-%m-%d_%H-%M-%S.log'.format(log_directory, fname)))
    file_handler.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('[%(asctime)s] %(name)s (%(levelname)s): %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    public_logger = logging.getLogger('Tool-Program.{}'.format(fname))
    public_logger.addHandler(file_handler)
    public_logger.addHandler(stream_handler)
    public_logger.setLevel(LOG_LEVEL)
    self_logger = logging.getLogger('Tool-Program.log')
    self_logger.addHandler(file_handler)
    self_logger.addHandler(stream_handler)
    self_logger.setLevel(LOG_LEVEL)

    return public_logger


# Logged decorator
def logged(cls, fname):
    self_logger.debug(f'Creating class-level logger for {cls.__name__}')
    class_name = cls.__name__
    logger = logging.getLogger('Tool-Program.{}.{}'.format(fname, class_name))
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    setattr(cls, 'logger', logger)
    return cls
