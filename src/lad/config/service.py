"""Configuration service for LAD."""

from lad.config.settings import Settings


class ConfigurationService:
    """Application configuration service."""

    def load(self) -> Settings:
        """Load application configuration."""
        return Settings()
