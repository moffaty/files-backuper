import logging
from logging.handlers import RotatingFileHandler
import sys
import os
from app.config import APP_SETTINGS

os.makedirs(APP_SETTINGS.log_dir, exist_ok=True)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = RotatingFileHandler(
    os.path.join(APP_SETTINGS.log_dir, APP_SETTINGS.log_file),
    maxBytes=1_000_000,
    backupCount=3,
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
