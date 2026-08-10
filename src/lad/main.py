"""Entry point for LAD."""

from lad.core.application import Application
from lad.modules.system import SystemModule


def main() -> None:
    """Start LAD application."""

    app = Application()

    logger = app.logging_service.get_logger()
    event_bus = app.event_bus
    registry = app.module_registry

    system_module = SystemModule(
        event_bus=event_bus,
        logger=logger,
    )

    registry.register(system_module)

    logger.info("Starting LAD")
    logger.info(f"Registered modules: {registry.count}")

    try:
        app.start()
        logger.info("Application started successfully")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
