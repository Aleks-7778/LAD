"""Tests for TaskRepository."""

from pathlib import Path

from lad.storage.schema import DatabaseSchema
from lad.storage.sqlite import SQLiteRepository
from lad.storage.tasks import TaskRepository


def create_task_repository(tmp_path: Path) -> tuple[
    SQLiteRepository,
    TaskRepository,
]:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    DatabaseSchema(repository).initialize()

    return repository, TaskRepository(repository)


def test_task_repository_creates_task(
    tmp_path: Path,
) -> None:
    repository, tasks = create_task_repository(tmp_path)

    task_id = tasks.create("Test task")

    assert task_id > 0

    task = tasks.get(task_id)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Test task"
    assert task["created_at"]
    assert task["updated_at"]

    repository.shutdown()


def test_task_repository_lists_tasks(
    tmp_path: Path,
) -> None:
    repository, tasks = create_task_repository(tmp_path)

    first_id = tasks.create("Task 1")
    second_id = tasks.create("Task 2")

    rows = tasks.list_all()

    assert [row["id"] for row in rows] == [
        first_id,
        second_id,
    ]
    assert [row["title"] for row in rows] == [
        "Task 1",
        "Task 2",
    ]

    repository.shutdown()


def test_task_repository_updates_task(
    tmp_path: Path,
) -> None:
    repository, tasks = create_task_repository(tmp_path)

    task_id = tasks.create("Old title")
    task_before = tasks.get(task_id)

    assert task_before is not None

    updated = tasks.update(
        task_id,
        "New title",
    )

    assert updated is True

    task_after = tasks.get(task_id)

    assert task_after is not None
    assert task_after["title"] == "New title"
    assert task_after["created_at"] == task_before["created_at"]
    assert task_after["updated_at"] >= task_before["updated_at"]

    repository.shutdown()


def test_task_repository_deletes_task(
    tmp_path: Path,
) -> None:
    repository, tasks = create_task_repository(tmp_path)

    task_id = tasks.create("Delete me")

    deleted = tasks.delete(task_id)

    assert deleted is True
    assert tasks.get(task_id) is None

    repository.shutdown()


def test_task_repository_returns_false_for_missing_task(
    tmp_path: Path,
) -> None:
    repository, tasks = create_task_repository(tmp_path)

    assert tasks.update(999, "Missing") is False
    assert tasks.delete(999) is False
    assert tasks.get(999) is None

    repository.shutdown()
