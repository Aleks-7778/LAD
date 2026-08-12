"""Runtime context for LAD."""

from __future__ import annotations

from dataclasses import dataclass

from lad.core.context import ApplicationContext
from lad.di.container import ServiceContainer
from lad.events.bus import EventBus
from lad.logging.service import LoggingService
from lad.modules.registry import ModuleRegistry
from lad.storage.sqlite import SQLiteRepository
from lad.storage.tasks import TaskRepository
from lad.config.settings import Settings


@dataclass(frozen=True)
class RuntimeContext(ApplicationContext):
    """Unified runtime dependencies of the LAD application."""

    task_repository: TaskRepository
    @property
    def services(self) -> ServiceContainer:
        """Alias for the application service container."""
        return self.container

    def get_logger(self, name: str | None = None):
        """Return an application logger."""
        return self.logging_service.get_logger(name)

    def shutdown(self) -> None:
        """Release runtime resources."""
        self.logging_service.shutdown()
        self.sqlite_repository.close()
