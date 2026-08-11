"""Tests for LAD database schema initialization."""

from pathlib import Path

from lad.storage.schema import DatabaseSchema
from lad.storage.sqlite import SQLiteRepository


def test_database_schema_initializes_tasks_table(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    schema = DatabaseSchema(repository)

    assert schema.initialized is False

    schema.initialize()

    assert schema.initialized is True

    row = repository.fetch_one(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'tasks'
        """
    )

    assert row is not None
    assert row["name"] == "tasks"

    repository.shutdown()


def test_database_schema_initialization_is_idempotent(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    schema = DatabaseSchema(repository)

    schema.initialize()
    schema.initialize()

    assert schema.initialized is True

    row = repository.fetch_one(
        """
        SELECT COUNT(*) AS count
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'tasks'
        """
    )

    assert row is not None
    assert row["count"] == 1

    repository.shutdown()


def test_database_schema_creates_expected_task_columns(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    schema = DatabaseSchema(repository)

    schema.initialize()

    rows = repository.fetch_all(
        "PRAGMA table_info(tasks)",
    )

    columns = {
        row["name"]
        for row in rows
    }

    assert columns == {
        "id",
        "title",
        "created_at",
        "updated_at",
    }

    repository.shutdown()


def test_database_schema_auto_connects_repository(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    schema = DatabaseSchema(repository)

    assert repository.connected is False

    schema.initialize()

    assert repository.connected is True
    assert repository.database_path.exists()

    repository.shutdown()
