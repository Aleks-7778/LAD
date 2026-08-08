from __future__ import annotations

from typing import Any


class ModuleRegistry:
    """Реестр модулей LAD."""

    def __init__(self, logger: Any | None = None) -> None:
        self._modules: dict[str, Any] = {}
        self._logger = logger
        self._started: set[str] = set()

    def register(self, module: Any, name: str | None = None) -> None:
        """Зарегистрировать модуль.

        Повторная регистрация имени запрещена.
        """

        module_name = name or self._module_name(module)

        if module_name in self._modules:
            raise ValueError(
                f"Module already registered: {module_name}"
            )

        self._modules[module_name] = module

        self._log(
            "info",
            f"Module registered: {module_name}",
        )

    def get(self, name: str) -> Any | None:
        """Получить модуль по имени."""

        return self._modules.get(name)

    def has(self, name: str) -> bool:
        """Проверить наличие модуля."""

        return name in self._modules

    @property
    def count(self) -> int:
        """Вернуть количество зарегистрированных модулей."""

        return len(self._modules)

    def names(self) -> tuple[str, ...]:
        """Вернуть имена зарегистрированных модулей."""

        return tuple(self._modules.keys())

    def start_all(self) -> None:
        """Запустить все модули один раз."""

        for name in self._modules:
            self.start(name)

    def stop_all(self) -> None:
        """Остановить все запущенные модули один раз."""

        for name in reversed(tuple(self._modules.keys())):
            self.stop(name)

    def start(self, name: str) -> bool:
        """Запустить модуль, если он ещё не запущен."""

        module = self._modules.get(name)

        if module is None:
            return False

        if name in self._started:
            return False

        start = getattr(module, "start", None)

        if not callable(start):
            return False

        self._log(
            "info",
            f"Starting module: {name}",
        )

        start()
        self._started.add(name)

        return True

    def stop(self, name: str) -> bool:
        """Остановить модуль, если он запущен."""

        module = self._modules.get(name)

        if module is None:
            return False

        if name not in self._started:
            return False

        stop = getattr(module, "stop", None)

        if not callable(stop):
            self._started.discard(name)
            return False

        self._log(
            "info",
            f"Stopping module: {name}",
        )

        stop()
        self._started.discard(name)

        return True

    def clear(self) -> None:
        """Удалить все зарегистрированные модули."""

        self._modules.clear()
        self._started.clear()

    @staticmethod
    def _module_name(module: Any) -> str:
        """Получить стабильное имя модуля."""

        name = getattr(module, "name", None)

        if isinstance(name, str) and name:
            return name

        return module.__class__.__name__

    def _log(self, level: str, message: str) -> None:
        """Безопасно отправить сообщение в logger."""

        if self._logger is None:
            return

        method = getattr(self._logger, level, None)

        if callable(method):
            method(message)