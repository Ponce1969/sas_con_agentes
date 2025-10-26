# backend/app/core/logger.py

import logging
import sys

def setup_logging():
    """Configurar logging básico para la aplicación."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

