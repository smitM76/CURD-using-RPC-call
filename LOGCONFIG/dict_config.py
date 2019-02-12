import logging
from logging.config import dictConfig
import json

file = open('./logging_config.ini', "r")
config = json.load(file)
