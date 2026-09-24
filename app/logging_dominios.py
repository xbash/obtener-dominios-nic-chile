"""Logger persistente para las consultas de dominios NIC Chile.

Version: v2.3
Agente/LLM: Claude Sonnet 5

Ver docs/04_DECISIONES_PENDIENTES.md para el contrato de eventos:
texto legible, rotacion por tamano, sin datos sensibles ni listas de
dominios completas.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.configuracion import (
    ARCHIVO_LOG,
    DIRECTORIO_LOGS,
    LOG_BACKUP_COUNT,
    LOG_MAX_BYTES,
    NOMBRE_LOGGER,
)

_FORMATO = "%(asctime)s | %(levelname)s | %(run_id)s | %(message)s"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger compartido, inicializandolo una sola vez.

    Idempotente: si ya tiene handlers, no vuelve a agregarlos (evita
    lineas duplicadas al invocarse desde app.main o wrappers).
    """
    logger = logging.getLogger(NOMBRE_LOGGER)
    if logger.handlers:
        return logger

    DIRECTORIO_LOGS.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        ARCHIVO_LOG,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(_FORMATO))

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
