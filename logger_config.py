"""Configuración del archivo de logs (eventos y errores)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def obtener_logger() -> logging.Logger:
    logger = logging.getLogger("SoftwareFJ")
    if not logger.handlers:
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"))
        logger.addHandler(handler)
    return logger
