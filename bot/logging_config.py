"""Logging configuration for the trading bot."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "trading_bot.log"

MAX_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure application logging with console and rotating file handlers.

    Creates the logs directory automatically if it does not exist.

    Args:
        level: Logging level for the application logger.

    Returns:
        logging.Logger: Configured root application logger.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a child logger under the trading_bot namespace.

    Args:
        name: Optional submodule name.

    Returns:
        logging.Logger: Logger instance.
    """
    setup_logging()
    if name:
        return logging.getLogger(f"trading_bot.{name}")
    return logging.getLogger("trading_bot")
