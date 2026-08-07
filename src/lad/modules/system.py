"""System module for LAD."""

from __future__ import annotations

from lad.modules.core import Module


class SystemModule(Module):
    """Base system module for LAD."""

    @property
    def name(self) -> str:
        """Return module name."""

        return "system"

    def start(self) -> None:
        """Start system module."""

        print("System module started")

    def stop(self) -> None:
        """Stop system module."""

        print("System module stopped")