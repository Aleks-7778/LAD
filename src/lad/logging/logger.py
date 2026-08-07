import logging
from pathlib import Path


def create_logger() -> logging.Logger:
    """Создает основной логгер приложения."""

    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("LAD")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logfile = logging.FileHandler(
        "logs/lad.log",
        encoding="utf-8"
    )
    logfile.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(logfile)

    return logger