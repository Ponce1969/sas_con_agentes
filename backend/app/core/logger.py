# backend/app/core/logger.py

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import settings

# Carpeta de logs
LOG_DIR = Path(settings.BASE_DIR) / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

# Formato estándar para todos los logs
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Logger principal
logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

# Rotating file handler (5 MB por archivo, 5 archivos de backup)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Stream handler (stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Evita duplicar handlers
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# Funciones utilitarias opcionales
def log_debug(msg: str, **kwargs):
    logger.debug(msg, extra=kwargs)

def log_info(msg: str, **kwargs):
    logger.info(msg, extra=kwargs)

def log_warning(msg: str, **kwargs):
    logger.warning(msg, extra=kwargs)

def log_error(msg: str, **kwargs):
    logger.error(msg, extra=kwargs)

def log_critical(msg: str, **kwargs):
    logger.critical(msg, extra=kwargs)

