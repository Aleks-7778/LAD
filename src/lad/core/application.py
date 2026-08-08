from __future__ import annotations

from typing import Any


class Application:
    """Главный жизненный цикл приложения LAD."""

    def __init__(
        self,
        logger: Any | None = None,
        module_registry: Any | None = None,
    ) -> None:
        self._logger = logger
        self._module_registry = module_registry

        self._initialized = False
        self._running = False

    @property
    def initialized(self) -> bool:
        """Возвращает состояние инициализации приложения."""

        return self._initialized

    @property
    def running(self) -> bool:
        """Возвращает состояние запущенного приложения."""

        return self._running

    def initialize(self) -> None:
        """Инициализировать приложение."""

        if self._initialized:
            return

        self._log(
            "info",
            "Initializing application",
        )

        self._initialized = True

    def start(self) -> None:
        """Запустить приложение."""

        if not self._initialized:
            self.initialize()

        if self._running:
            return

        self._log(
            "info",
            "Starting application",
        )

        if self._module_registry is not None:
            self._module_registry.start_all()

        self._running = True

        self._log(
            "info",
            "Application started successfully",
        )

    def stop(self) -> None:
        """Остановить приложение."""

        if not self._running:
            return

        self._log(
            "info",
            "Stopping application",
        )

        if self._module_registry is not None:
            self._module_registry.stop_all()

        self._running = False

        self._log(
            "info",
            "Application stopped",
        )

    def shutdown(self) -> None:
        """Полностью завершить работу приложения."""

        if self._running:
            self.stop()

        if not self._initialized:
            return

        self._log(
            "info",
            "Shutting down application",
        )

        self._initialized = False

    def _log(
        self,
        level: str,
        message: str,
    ) -> None:
        """Безопасно отправить сообщение в logger."""

        if self._logger is None:
            return

        method = getattr(
            self._logger,
            level,
            None,
        )

        if callable(method):
            method(message)