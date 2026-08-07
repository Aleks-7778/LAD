"""Core module abstractions for LAD."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Module(ABC):
    """Base class for every LAD module."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique module name."""

    def start(self) -> None:
        """Start the module."""

    def stop(self) -> None:
        """Stop the module."""