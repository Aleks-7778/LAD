"""Tests for SQLiteRepository."""

from pathlib import Path

from lad.storage.sqlite import SQLiteRepository


def test_repository_connects_and_creates_database(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lad.db"

    repository = SQLiteRepository(str(database_path))

    assert repository.connected is False

    repository.connect()

    assert repository.connected is True
    assert database_path.exists()

    repository.shutdown()


def test_repository_executes_sql_and_fetches_rows(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lad.db"
    repository = SQLiteRepository(str(database_path))

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    repository.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        ("Test task",),
    )

    row = repository.fetch_one(
        "SELECT id, title FROM tasks WHERE title = ?",
        ("Test task",),
    )

    assert row is not None
    assert row["title"] == "Test task"

    repository.shutdown()


def test_repository_fetch_all(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    repository.executemany(
        "INSERT INTO tasks (title) VALUES (?)",
        [
            ("Task 1",),
            ("Task 2",),
            ("Task 3",),
        ],
    )

    rows = repository.fetch_all(
        "SELECT title FROM tasks ORDER BY id",
    )

    assert [row["title"] for row in rows] == [
        "Task 1",
        "Task 2",
        "Task 3",
    ]

    repository.shutdown()


def test_repository_shutdown_is_idempotent(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    repository.connect()

    assert repository.connected is True

    repository.shutdown()
    repository.shutdown()

    assert repository.connected is False


def test_repository_reconnects_after_shutdown(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lad.db"
    repository = SQLiteRepository(str(database_path))

    repository.connect()
    repository.shutdown()

    assert repository.connected is False

    repository.connect()

    assert repository.connected is True

    repository.shutdown()


def test_repository_exposes_database_path(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "storage" / "lad.db"
    repository = SQLiteRepository(str(database_path))

    assert repository.database_path == database_path

    repository.shutdown()


def test_repository_execute_auto_connects(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lad.db"
    repository = SQLiteRepository(str(database_path))

    assert repository.connected is False

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    assert repository.connected is True
    assert database_path.exists()

    repository.shutdown()


def test_repository_fetch_auto_connects(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "lad.db"
    repository = SQLiteRepository(str(database_path))

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    repository.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        ("Auto connect",),
    )

    repository.shutdown()

    assert repository.connected is False

    row = repository.fetch_one(
        "SELECT title FROM tasks WHERE title = ?",
        ("Auto connect",),
    )

    assert row is not None
    assert row["title"] == "Auto connect"
    assert repository.connected is True

    repository.shutdown()


def test_repository_can_execute_after_shutdown(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    repository.shutdown()

    repository.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        ("After shutdown",),
    )

    row = repository.fetch_one(
        "SELECT title FROM tasks WHERE title = ?",
        ("After shutdown",),
    )

    assert row is not None
    assert row["title"] == "After shutdown"

    repository.shutdown()


def test_repository_transaction_commits_on_success(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    with repository.transaction():
        repository.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            ("Transaction task",),
        )

    row = repository.fetch_one(
        "SELECT title FROM tasks WHERE title = ?",
        ("Transaction task",),
    )

    assert row is not None
    assert row["title"] == "Transaction task"

    repository.shutdown()


def test_repository_transaction_rolls_back_on_failure(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    repository.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )

    try:
        with repository.transaction():
            repository.execute(
                "INSERT INTO tasks (title) VALUES (?)",
                ("Rollback task",),
            )
            raise RuntimeError("transaction failed")
    except RuntimeError as exc:
        assert str(exc) == "transaction failed"

    row = repository.fetch_one(
        "SELECT title FROM tasks WHERE title = ?",
        ("Rollback task",),
    )

    assert row is None

    repository.shutdown()


def test_repository_transaction_auto_connects(
    tmp_path: Path,
) -> None:
    repository = SQLiteRepository(
        str(tmp_path / "lad.db"),
    )

    with repository.transaction():
        repository.execute(
            """
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
            """
        )

        repository.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            ("Auto transaction",),
        )

    assert repository.connected is True

    row = repository.fetch_one(
        "SELECT title FROM tasks WHERE title = ?",
        ("Auto transaction",),
    )

    assert row is not None
    assert row["title"] == "Auto transaction"

    repository.shutdown()
