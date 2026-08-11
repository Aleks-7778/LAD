"""Task repository for LAD."""

from __future__ import annotations

from datetime import datetime, timezone

from lad.storage.sqlite import SQLiteRepository


class TaskRepository:
    """Repository for task persistence."""

    def __init__(self, repository: SQLiteRepository) -> None:
        self._repository = repository

    def create(self, title: str) -> int:
        """Create a task and return its identifier."""

        now = datetime.now(timezone.utc).isoformat()

        cursor = self._repository.execute(
            """
            INSERT INTO tasks (
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?)
            """,
            (title, now, now),
        )

        assert cursor.lastrowid is not None
        return int(cursor.lastrowid)

    def get(self, task_id: int):
        """Return a task by identifier."""

        return self._repository.fetch_one(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )

    def list_all(self):
        """Return all tasks ordered by identifier."""

        return self._repository.fetch_all(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM tasks
            ORDER BY id
            """
        )

    def update(self, task_id: int, title: str) -> bool:
        """Update a task title."""

        now = datetime.now(timezone.utc).isoformat()

        cursor = self._repository.execute(
            """
            UPDATE tasks
            SET
                title = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (title, now, task_id),
        )

        return cursor.rowcount > 0

    def delete(self, task_id: int) -> bool:
        """Delete a task."""

        cursor = self._repository.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )

        return cursor.rowcount > 0
