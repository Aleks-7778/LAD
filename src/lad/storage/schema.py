"""Database schema initialization for LAD."""

from __future__ import annotations

from lad.storage.sqlite import SQLiteRepository


class DatabaseSchema:
    """Initialize and maintain the LAD database schema."""

    def __init__(self, repository: SQLiteRepository) -> None:
        self._repository = repository
        self._initialized = False

    @property
    def initialized(self) -> bool:
        """Return True when the schema has been initialized."""

        return self._initialized

    def initialize(self) -> None:
        """Initialize the database schema."""

        if self._initialized:
            return

        with self._repository.transaction():
            self._repository.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

        self._initialized = True
