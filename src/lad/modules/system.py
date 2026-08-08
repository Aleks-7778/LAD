from __future__ import annotations

from typing import Any


class SystemModule:
    """
    Системный модуль LAD.

    Отвечает за базовый жизненный цикл системного модуля
    и является первым реальным модулем, подключаемым к ModuleRegistry.
    """

    name = "system"

    def __init__(
        self,
        event_bus: Any,
        logger: Any,
    ) -> None:
        self._event_bus = event_bus
        self._logger = logger
        self._started = False

    @property
    def started(self) -> bool:
        """Возвращает состояние модуля."""
        return self._started

    def start(self) -> None:
        """Запустить системный модуль."""
        if self._started:
            return

        self._started = True

        self._logger.info("System module started")

    def stop(self) -> None:
        """Остановить системный модуль."""
        if not self._started:
            return

        self._started = False

        self._logger.info("System module stopped")