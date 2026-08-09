from lad.config.service import ConfigurationService
from lad.config.settings import Settings


def test_configuration_service_loads_default_settings() -> None:
    service = ConfigurationService()

    settings = service.load()

    assert isinstance(settings, Settings)
    assert settings.app_name == "LAD"
    assert settings.version == "0.1.0-alpha.3"
