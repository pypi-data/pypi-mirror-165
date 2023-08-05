"""
The pipeline module containing extract, preprocess and train
"""
import logging

from houses_pipeline.config import config
from houses_pipeline.config import logging_configuration
from houses_pipeline.constants import PACKAGE_ROOT

VERSION_PATH = PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging_config.get_console_handler())
# logger.propagate = False


with open(VERSION_PATH, 'r', encoding='utf-8') as version_file:
    __version__ = version_file.read().strip()
