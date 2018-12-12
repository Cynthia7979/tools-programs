import logging
from time import strftime

def log_init(fname):
    if not fname:
        fname = 'tool-program'
    file_handler = logging.FileHander(strftime('Logs/{}_log_%y-%m-%d_%H-%M-%S.log'.format(fname)))
    file_handler.setLevel(get_level())
    formatter = logging.Formatter('[%(asctime)s] %(name)s (%(levelname)s): %(message)s')
    file_handler.setFormatter(formatter)
    public_logger = logging.getLogger('Tool-Program.{}'.format(fname))


def get_level():
    d = {'debug': logging.DEBUG,
         'info': logging.INFO,
         'warning': logging.WARNING,
         'error': logging.ERROR,
         'critical': logging.CRITICAL}
    f = open('debug')
    t = f.read()
    if t in d.keys(): return d[t]
    else: return logging.WARNING


# Logged decorator
def logged(cls, fname):
    class_name = cls.__name__
    logger = logging.getLogger('Tool-Program.{}.{}'.format(fname, cls))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.propagate = False
    setattr(cls, 'logger', logger)
    return cls