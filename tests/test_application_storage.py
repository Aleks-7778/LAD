"""Tests for application SQLite storage integration."""

from pathlib import Path

from lad.core.application import Application
from lad.storage.sqlite import SQLiteRepository


def test_application_registers_sqlite_repository() -> None:
    app = Application()

    app.initialize()

    assert (
        app.service_container.resolve(SQLiteRepository)
        is app.sqlite_repository
    )


def test_application_starts_sqlite_repository(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    app = Application(
        sqlite_repository=repository,
    )

    app.start()

    assert app.running is True
    assert repository.connected is True

    app.stop()

    assert repository.connected is False


def test_application_shutdown_closes_sqlite_repository(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    app = Application(
        sqlite_repository=repository,
    )

    app.start()

    assert repository.connected is True

    app.shutdown()

    assert app.initialized is False
    assert app.running is False
    assert repository.connected is False
