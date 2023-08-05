import logging
import os
from kolibri.default_configs import DO_LOG
from kolibri.default_configs import LOG_NAME, LOG_LEVEL, LOGS_DIR


def get_logger(module_name=LOG_NAME, log_level=LOG_LEVEL):
    if not DO_LOG:
        return None

    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    fh = logging.FileHandler(os.path.join(LOGS_DIR, module_name + '.log'))
    if os.environ.get('KOLIBRI_DEV') == 'True':
        log_format = '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)d - %(message)s'
    else:
        log_format = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'

    fh.setFormatter(logging.Formatter(log_format))
    fh.setLevel(log_level)
    logger.addHandler(fh)
    return logger


if __name__ == "__main__":
    pass
