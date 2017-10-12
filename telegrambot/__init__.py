from os import path
from logging import getLogger
from logging.config import fileConfig
log_file_path = path.join(path.dirname(path.abspath(__file__)), '..', 'logging_config.ini')
fileConfig(log_file_path)

__version__ = '1.0.2'
