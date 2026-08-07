"""
Application Core.

Главная точка управления приложением ЛАД.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Application:
    """
    Основной класс приложения.
    """

    name: str = "LAD"
    version: str = "0.1.0-alpha.2"

    def start(self) -> None:
        """Запуск приложения."""
        print(f"{self.name} {self.version} started")

    def stop(self) -> None:
        """Остановка приложения."""
        print(f"{self.name} stopped")