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
from lad.storage.sqlite import SQLiteRepository


class Application:
    """Главный жизненный цикл приложения LAD."""

    def __init__(
        self,
        event_bus: EventBus | None = None,
        module_registry: ModuleRegistry | None = None,
        service_container: ServiceContainer | None = None,
        configuration_service: ConfigurationService | None = None,
        logging_service: LoggingService | None = None,
        sqlite_repository: SQLiteRepository | None = None,
    ) -> None:
        self._initialized = False
        self._running = False

        self._service_container = (
            service_container or ServiceContainer()
        )

        self._event_bus = event_bus or EventBus()
        self._module_registry = module_registry or ModuleRegistry()
        self._configuration_service = (
            configuration_service or ConfigurationService()
        )

        self._logging_service = logging_service
        self._sqlite_repository = sqlite_repository
        self._settings: Settings | None = None

        # Core services available immediately.
        self._service_container.register(
            EventBus,
            self._event_bus,
        )
        self._service_container.register(
            ModuleRegistry,
            self._module_registry,
        )
        self._service_container.register(
            ConfigurationService,
            self._configuration_service,
        )

        # LoggingService is initialized immediately so that
        # Application() exposes a valid logging service and DI
        # can resolve it before initialize().
        if self._logging_service is None:
            self._logging_service = LoggingService(
                Settings(),
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

        if self._logging_service is None:
            raise RuntimeError(
                "LoggingService is not initialized"
            )

        return self._logging_service

    @property
    def sqlite_repository(self) -> SQLiteRepository:
        """Возвращает SQLite repository приложения."""

        if self._sqlite_repository is None:
            raise RuntimeError(
                "SQLiteRepository is not initialized"
            )

        return self._sqlite_repository

    @property
    def settings(self) -> Settings | None:
        """Возвращает загруженные настройки приложения."""

        return self._settings

    def initialize(self) -> None:
        """Инициализировать приложение."""

        if self._initialized:
            return

        self._settings = self._configuration_service.load()

        # Recreate logging service from actual application settings.
        if self._logging_service is not None:
            self._logging_service.shutdown()

        self._logging_service = LoggingService(
            self._settings,
        )

        if self._sqlite_repository is None:
            self._sqlite_repository = SQLiteRepository(
                self._settings.database_path,
            )

        self._service_container.register(
            Settings,
            self._settings,
        )
        self._service_container.register(
            LoggingService,
            self._logging_service,
        )
        self._service_container.register(
            SQLiteRepository,
            self._sqlite_repository,
        )

        self._initialized = True

    def start(self) -> None:
        """Запустить приложение."""

        if not self._initialized:
            self.initialize()

        if self._running:
            return

        self._event_bus.publish(ApplicationStarting())

        if self._sqlite_repository is None:
            raise RuntimeError(
                "SQLiteRepository is not initialized"
            )

        self._sqlite_repository.connect()
        self._module_registry.start_all()

        self._running = True

        self._event_bus.publish(ApplicationStarted())

    def stop(self) -> None:
        """Остановить приложение."""

        if not self._running:
            return

        self._event_bus.publish(ApplicationStopping())

        self._module_registry.stop_all()

        if self._sqlite_repository is not None:
            self._sqlite_repository.close()

        self._running = False

        self._event_bus.publish(ApplicationStopped())

    def shutdown(self) -> None:
        """Полностью завершить работу приложения."""

        if self._running:
            self.stop()

        if self._logging_service is not None:
            self._logging_service.shutdown()

        if self._sqlite_repository is not None:
            self._sqlite_repository.close()

        self._initialized = False
        self._settings = None
