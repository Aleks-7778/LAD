"""Entry point for LAD."""

from lad.config.service import ConfigurationService
from lad.logging.service import LoggingService
from lad.core.application import Application
from lad.di.container import Container
from lad.events.bus import EventBus
from lad.modules.registry import ModuleRegistry
from lad.modules.system import SystemModule


def main() -> None:
    """Start LAD application."""

    container = Container()

    # Register core services.
    container.register(ConfigurationService)
    container.register(LoggingService)

    # Resolve core services.
    config = container.resolve(ConfigurationService)
    logger = container.resolve(LoggingService)

    settings = config.load()

    logger.info("Starting LAD")

    # Create event bus.
    event_bus = EventBus()

    # Create module registry.
    registry = ModuleRegistry()

    # Register system module.
    system_module = SystemModule(
        event_bus=event_bus,
        logger=logger,
    )

    registry.register(system_module)

    logger.info(f"Registered modules: {registry.count}")

    # Start modules.
    registry.start_all()

    # Create and configure application.
    app = Application()
    app.name = settings.app_name
    app.version = settings.version

    # Start application.
    app.start()

    logger.info("Application started successfully")

    # Current lifecycle is intentionally lightweight.
    # Modules remain available for the application lifecycle.
    registry.stop_all()


if __name__ == "__main__":
    main()
