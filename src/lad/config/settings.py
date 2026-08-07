from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "LAD"
    version: str = "0.1.0-alpha.3"