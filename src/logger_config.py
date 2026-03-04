"""
Módulo centralizado de configuración de logging para el challenge.

Formato de log: YYYY-MM-DD HH-MM-SS [FILENAME] MESSAGE

Uso:
    from logger_config import get_logger
    logger = get_logger(__name__)
    logger.info("Processing started")
"""

import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Crea y retorna un logger configurado con el formato del proyecto.

    Args:
        name: Nombre del módulo (usar __name__).
        level: Nivel de logging (default: INFO).

    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(name)

    # Evitar agregar handlers duplicados si se llama varias veces
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Formato: YYYY-MM-DD HH-MM-SS [FILENAME] MESSAGE
    # Se usa %(filename)s para obtener automáticamente el nombre del archivo
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(filename)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
