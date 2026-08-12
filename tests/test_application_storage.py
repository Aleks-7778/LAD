"""Tests for application SQLite storage integration."""

from pathlib import Path

from lad.core.application import Application
from lad.storage.schema import DatabaseSchema
from lad.storage.sqlite import SQLiteRepository
from lad.storage.tasks import TaskRepository


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


def test_application_registers_database_schema() -> None:
    app = Application()

    app.initialize()

    assert (
        app.service_container.resolve(DatabaseSchema)
        is app.database_schema
    )

    app.shutdown()


def test_application_initializes_database_schema_on_start(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    app = Application(
        sqlite_repository=repository,
    )

    app.start()

    assert app.database_schema.initialized is True

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

    app.stop()


def test_application_accepts_database_schema_dependency(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    schema = DatabaseSchema(repository)

    app = Application(
        sqlite_repository=repository,
        database_schema=schema,
    )

    app.initialize()

    assert app.database_schema is schema

    app.shutdown()


def test_application_registers_task_repository() -> None:
    app = Application()

    app.initialize()

    assert (
        app.service_container.resolve(TaskRepository)
        is app.task_repository
    )

    app.shutdown()


def test_application_accepts_task_repository_dependency(
    tmp_path: Path,
) -> None:

    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    task_repository = TaskRepository(repository)

    app = Application(
        sqlite_repository=repository,
        task_repository=task_repository,
    )

    app.initialize()

    assert app.task_repository is task_repository
    assert (
        app.service_container.resolve(TaskRepository)
        is task_repository
    )

    app.shutdown()


def test_application_task_repository_works_after_start(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    app = Application(
        sqlite_repository=repository,
    )

    app.start()

    task_id = app.task_repository.create("Application task")

    task = app.task_repository.get(task_id)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Application task"

    app.shutdown()


def test_application_context_exposes_task_repository() -> None:
    app = Application()

    app.initialize()

    assert app.context.task_repository is app.task_repository
    assert (
        app.context.task_repository
        is app.service_container.resolve(TaskRepository)
    )

    app.shutdown()


def test_application_context_task_repository_works_after_start(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )
    app = Application(
        sqlite_repository=repository,
    )

    app.start()

    task_id = app.context.task_repository.create(
        "Runtime context task",
    )

    task = app.context.task_repository.get(task_id)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Runtime context task"

    app.shutdown()
