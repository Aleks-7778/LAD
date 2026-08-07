"""
Entry point for LAD.
"""

from lad.config.service import ConfigurationService
from lad.core.application import Application


def main() -> None:
    config = ConfigurationService()
    settings = config.load()

    app = Application()
    app.name = settings.app_name
    app.version = settings.version

    app.start()


if __name__ == "__main__":
    main()