"""Application lifecycle for LAD."""

from __future__ import annotations

from lad.config.service import ConfigurationService
from lad.config.settings import Settings
from lad.di.container import ServiceContainer
from lad.events.application import (
    ApplicationStarted,
    ApplicationStarting,
    ApplicationStopped,
    ApplicationStopping,
)
from lad.events.bus import EventBus
from lad.logging.service import LoggingService
from lad.modules.registry import ModuleRegistry


class Application:
    """Главный жизненный цикл приложения LAD."""

    def __init__(
        self,
        event_bus: EventBus | None = None,
        module_registry: ModuleRegistry | None = None,
        service_container: ServiceContainer | None = None,
        configuration_service: ConfigurationService | None = None,
        logging_service: LoggingService | None = None,
    ) -> None:
        self._initialized = False
        self._running = False

        self._service_container = service_container or ServiceContainer()

        self._event_bus = event_bus or EventBus()
        self._module_registry = module_registry or ModuleRegistry()
        self._configuration_service = (
            configuration_service or ConfigurationService()
        )
        self._logging_service = logging_service or LoggingService()
        self._settings: Settings | None = None

        self._service_container.register(EventBus, self._event_bus)
        self._service_container.register(
            ModuleRegistry,
            self._module_registry,
        )
        self._service_container.register(
            ConfigurationService,
            self._configuration_service,
        )
        self._service_container.register(
            LoggingService,
            self._logging_service,
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

    @property
    def configuration_service(self) -> ConfigurationService:
        """Возвращает сервис конфигурации приложения."""

        return self._configuration_service

    @property
    def logging_service(self) -> LoggingService:
        """Возвращает сервис логирования приложения."""

        return self._logging_service

    @property
    def settings(self) -> Settings | None:
        """Возвращает загруженные настройки приложения."""

        return self._settings

    def initialize(self) -> None:
        """Инициализировать приложение."""

        if self._initialized:
            return

        self._settings = self._configuration_service.load()

        self._logging_service.shutdown()
        self._logging_service = LoggingService(self._settings)

        self._service_container.register(
            LoggingService,
            self._logging_service,
        )

        self._logging_service.logger.info(
            "Initializing application %s",
            self._settings.version,
        )

        self._service_container.register(Settings, self._settings)

        self._initialized = True

    def start(self) -> None:
        """Запустить приложение."""

        if not self._initialized:
            self.initialize()

        if self._running:
            return

        self._logging_service.logger.info("Starting application")

        self._event_bus.publish(ApplicationStarting())

        self._module_registry.start_all()
        self._running = True

        self._event_bus.publish(ApplicationStarted())

        self._logging_service.logger.info("Application started")

    def stop(self) -> None:
        """Остановить приложение."""

        if not self._running:
            return

        self._logging_service.logger.info("Stopping application")

        self._event_bus.publish(ApplicationStopping())

        self._module_registry.stop_all()
        self._running = False

        self._event_bus.publish(ApplicationStopped())

        self._logging_service.logger.info("Application stopped")

    def shutdown(self) -> None:
        """Полностью завершить работу приложения."""

        if self._running:
            self.stop()

        if self._initialized:
            self._logging_service.logger.info("Shutting down application")

        self._logging_service.shutdown()

        self._initialized = False
        self._settings = None
