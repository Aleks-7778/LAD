"""Application lifecycle for LAD."""

from __future__ import annotations

from lad.di.container import ServiceContainer
from lad.events.application import (
    ApplicationStarted,
    ApplicationStarting,
    ApplicationStopped,
    ApplicationStopping,
)
from lad.events.bus import EventBus
from lad.modules.registry import ModuleRegistry


class Application:
    """Главный жизненный цикл приложения LAD."""

    def __init__(
        self,
        event_bus: EventBus | None = None,
        module_registry: ModuleRegistry | None = None,
        service_container: ServiceContainer | None = None,
    ) -> None:
        self._initialized = False
        self._running = False

        self._service_container = service_container or ServiceContainer()

        self._event_bus = event_bus or EventBus()
        self._module_registry = module_registry or ModuleRegistry()

        self._service_container.register(EventBus, self._event_bus)
        self._service_container.register(
            ModuleRegistry,
            self._module_registry,
        )

    @property
    def initialized(self) -> bool:
        """Возвращает True, если приложение инициализировано."""

        return self._initialized

    @property
    def running(self) -> bool:
        """Возвращает True, если приложение запущено."""

        return self._running

    @property
    def event_bus(self) -> EventBus:
        """Возвращает шину событий приложения."""

        return self._event_bus

    @property
    def module_registry(self) -> ModuleRegistry:
        """Возвращает реестр модулей приложения."""

        return self._module_registry

    @property
    def service_container(self) -> ServiceContainer:
        """Возвращает контейнер сервисов приложения."""

        return self._service_container

    def initialize(self) -> None:
        """Инициализировать приложение."""

        if self._initialized:
            return

        self._initialized = True

    def start(self) -> None:
        """Запустить приложение."""

        if not self._initialized:
            self.initialize()

        if self._running:
            return

        self._event_bus.publish(ApplicationStarting())

        self._module_registry.start_all()
        self._running = True

        self._event_bus.publish(ApplicationStarted())

    def stop(self) -> None:
        """Остановить приложение."""

        if not self._running:
            return

        self._event_bus.publish(ApplicationStopping())

        self._module_registry.stop_all()
        self._running = False

        self._event_bus.publish(ApplicationStopped())

    def shutdown(self) -> None:
        """Полностью завершить работу приложения."""

        if self._running:
            self.stop()

        self._initialized = False