"""Entry point for LAD."""

from lad.config.service import ConfigurationService
from lad.logging.service import LoggingService
from lad.di.container import Container
from lad.core.application import Application
from lad.modules.registry import ModuleRegistry
from lad.modules.system import SystemModule


def main() -> None:
    """Start LAD."""

    container = Container()

    container.register(ConfigurationService)
    container.register(LoggingService)

    config = container.resolve(ConfigurationService)
    logger = container.resolve(LoggingService)

    settings = config.load()

    logger.info("Starting LAD")

    app = Application()
    app.name = settings.app_name
    app.version = settings.version

    registry = ModuleRegistry()

    system_module = SystemModule()
    registry.register(system_module)

    logger.info(
        f"Registered modules: {registry.count()}"
    )

    registry.start_all()

    app.start()

    logger.info("Application started successfully")

    registry.stop_all()


if __name__ == "__main__":
    main()