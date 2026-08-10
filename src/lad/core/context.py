"""Application context for LAD."""

from __future__ import annotations

from dataclasses import dataclass

from lad.config.settings import Settings
from lad.di.container import ServiceContainer
from lad.events.bus import EventBus
from lad.logging.service import LoggingService
from lad.modules.registry import ModuleRegistry
from lad.storage.sqlite import SQLiteRepository


@dataclass(frozen=True)
class ApplicationContext:
    """Central context containing initialized LAD services."""

    settings: Settings
    container: ServiceContainer
    event_bus: EventBus
    module_registry: ModuleRegistry
    logging_service: LoggingService
    sqlite_repository: SQLiteRepository
