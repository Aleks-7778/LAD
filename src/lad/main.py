"""
Entry point for LAD.
"""

from lad.config.service import ConfigurationService
from lad.logging.service import LoggingService
from lad.core.application import Application


def main() -> None:
    config = ConfigurationService()
    settings = config.load()

    logger = LoggingService()
    logger.info("Starting LAD")

    app = Application()
    app.name = settings.app_name
    app.version = settings.version

    app.start()

    logger.info("Application started successfully")


if __name__ == "__main__":
    main()