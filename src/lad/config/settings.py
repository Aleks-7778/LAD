"""Application settings for LAD."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application configuration settings."""

    app_name: str = "LAD"
    version: str = "0.1.0-alpha.3"
    logging_level: str = "INFO"
    logging_file: str = "logs/lad.log"
