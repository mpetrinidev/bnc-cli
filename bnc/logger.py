import logging
import os

import json_log_formatter

from bnc.utils.config import read_configuration

formatter = json_log_formatter.JSONFormatter()
filename = os.path.join(os.path.expanduser("~"), read_configuration()["bnc_config_path"], "logs", "log.json")
os.makedirs(os.path.dirname(filename), exist_ok=True)

json_handler = logging.FileHandler(filename=filename)
json_handler.setFormatter(formatter)

logger = logging.getLogger('bnc_logger')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)
