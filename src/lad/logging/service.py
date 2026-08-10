"""Logging service for LAD."""

from __future__ import annotations

import logging
from pathlib import Path

from lad.config.settings import Settings


class LoggingService:
    """Centralized application logging service."""

    LOGGER_NAME = "lad"

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or Settings()
        self._configured = False
        self._logger = logging.getLogger(self.LOGGER_NAME)

    @property
    def logger(self) -> logging.Logger:
        """Return the LAD root logger."""

        return self._logger

    @property
    def configured(self) -> bool:
        """Return True when logging is configured."""

        return self._configured

    def configure(self) -> None:
        """Configure the LAD logging system."""

        if self._configured:
            return

        log_path = Path(self._settings.logging_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        level = getattr(
            logging,
            self._settings.logging_level.upper(),
            logging.INFO,
        )

        self._logger.setLevel(level)
        self._logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_path,
            mode="a",
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)

        self._configured = True

    def get_logger(
        self,
        name: str | None = None,
    ) -> logging.Logger:
        """Return a logger for the application or a named component."""

        if not self._configured:
            self.configure()

        if not name:
            return self._logger

        return logging.getLogger(f"{self.LOGGER_NAME}.{name}")

    def shutdown(self) -> None:
        """Close and remove LAD logging handlers."""

        for handler in list(self._logger.handlers):
            handler.flush()
            handler.close()
            self._logger.removeHandler(handler)

        self._configured = False
