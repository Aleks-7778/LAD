from lad.config.settings import Settings


class ConfigurationService:
    """Configuration Service."""

    def load(self) -> Settings:
        """
        Загрузка конфигурации.
        Пока используются значения по умолчанию.
        """

        return Settings()