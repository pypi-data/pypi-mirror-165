import logging
import os
import sys
try:
    import psutil
except ImportError:
    psutil = None
import tempfile


def logger(package, userspace=False, only_stdout=False):
    """
    TODO: need a documentation
    """
    logger = logging.getLogger(package)
    logger.setLevel(logging.DEBUG)

    if not only_stdout:
        if userspace:
            if psutil:
                current_user = psutil.Process().username().lower()
            else:
                current_user = os.getlogin()

            # Remove Windows domain if needed
            if '\\' in current_user:
                current_user = current_user.split('\\')[1]

            if sys.platform.startswith('win'):
                logfile = os.path.join(os.environ['USERPROFILE'], 'WAPT', package + '.log')
            else:
                logfile = os.path.join(tempfile.gettempdir(), 'WAPT.{}'.format(current_user), package + '.log')

            # remove all handlers
            logger.handlers = []
        else:
            if sys.platform.startswith('win'):
                logfile = os.path.join(os.environ['SYSTEMROOT'], 'WAPT', package + '.log')
            else:
                logfile = os.path.join(tempfile.gettempdir(), 'WAPT', package + '.log')

        if not os.path.isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
