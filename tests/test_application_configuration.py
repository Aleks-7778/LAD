from lad.config.service import ConfigurationService
from lad.config.settings import Settings
from lad.core.application import Application


def test_application_registers_configuration_service() -> None:
    application = Application()

    assert application.configuration_service is not None
    assert (
        application.service_container.resolve(ConfigurationService)
        is application.configuration_service
    )


def test_application_loads_settings_during_initialization() -> None:
    application = Application()

    assert application.settings is None

    application.initialize()

    assert application.settings is not None
    assert isinstance(application.settings, Settings)
    assert application.settings.app_name == "LAD"
    assert application.service_container.resolve(Settings) is application.settings


def test_application_accepts_custom_configuration_service() -> None:
    configuration_service = ConfigurationService()
    application = Application(
        configuration_service=configuration_service,
    )

    assert application.configuration_service is configuration_service
    assert (
        application.service_container.resolve(ConfigurationService)
        is configuration_service
    )
