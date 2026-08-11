"""SQLite repository for LAD."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


class SQLiteRepository:
    """Local SQLite storage repository."""

    def __init__(self, database_path: str = "data/lad.db") -> None:
        self._database_path = Path(database_path)
        self._connection: sqlite3.Connection | None = None
        self._transaction_depth = 0

    @property
    def database_path(self) -> Path:
        """Return the configured database path."""

        return self._database_path

    @property
    def connected(self) -> bool:
        """Return True when a database connection is active."""

        return self._connection is not None

    def connect(self) -> None:
        """Open the SQLite database connection."""

        if self._connection is not None:
            return

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self._database_path,
        )
        self._connection.row_factory = sqlite3.Row

    def execute(
        self,
        sql: str,
        parameters: Sequence[Any] = (),
    ) -> sqlite3.Cursor:
        """Execute a SQL statement."""

        self._ensure_connected()

        assert self._connection is not None

        cursor = self._connection.execute(
            sql,
            parameters,
        )

        if self._transaction_depth == 0:
            self._connection.commit()

        return cursor

    def executemany(
        self,
        sql: str,
        parameters: Iterable[Sequence[Any]],
    ) -> sqlite3.Cursor:
        """Execute a SQL statement for multiple parameter sets."""

        self._ensure_connected()

        assert self._connection is not None

        cursor = self._connection.executemany(
            sql,
            parameters,
        )

        if self._transaction_depth == 0:
            self._connection.commit()

        return cursor

    def fetch_one(
        self,
        sql: str,
        parameters: Sequence[Any] = (),
    ) -> sqlite3.Row | None:
        """Fetch a single row."""

        cursor = self.execute(sql, parameters)
        return cursor.fetchone()

    def fetch_all(
        self,
        sql: str,
        parameters: Sequence[Any] = (),
    ) -> list[sqlite3.Row]:
        """Fetch all rows."""

        cursor = self.execute(sql, parameters)
        return cursor.fetchall()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Execute operations inside a transaction."""

        self._ensure_connected()

        assert self._connection is not None

        outermost = self._transaction_depth == 0
        self._transaction_depth += 1

        if outermost:
            self._connection.execute("BEGIN")

        try:
            yield
        except Exception:
            self._transaction_depth -= 1

            if outermost:
                self._connection.rollback()

            raise
        else:
            self._transaction_depth -= 1

            if outermost:
                self._connection.commit()

    def close(self) -> None:
        """Close the database connection."""

        if self._connection is None:
            return

        self._connection.close()
        self._connection = None
        self._transaction_depth = 0

    def shutdown(self) -> None:
        """Shutdown the repository."""

        self.close()

    def _ensure_connected(self) -> None:
        if self._connection is None:
            self.connect()
