"""Module registry for LAD."""

from __future__ import annotations

from typing import Dict

from lad.modules.core import Module


class ModuleRegistry:
    """Registry responsible for LAD module lifecycle."""

    def __init__(self) -> None:
        self._modules: Dict[str, Module] = {}

    def register(self, module: Module) -> None:
        """Register a module."""

        if module.name in self._modules:
            raise ValueError(
                f"Module already registered: {module.name}"
            )

        self._modules[module.name] = module

    def get(self, name: str) -> Module:
        """Return a registered module by name."""

        try:
            return self._modules[name]
        except KeyError as exc:
            raise KeyError(
                f"Module not registered: {name}"
            ) from exc

    def has(self, name: str) -> bool:
        """Return True when a module is registered."""

        return name in self._modules

    def all(self) -> tuple[Module, ...]:
        """Return all registered modules."""

        return tuple(self._modules.values())

    def start_all(self) -> None:
        """Start all registered modules."""

        for module in self._modules.values():
            module.start()

    def stop_all(self) -> None:
        """Stop all registered modules in reverse order."""

        for module in reversed(tuple(self._modules.values())):
            module.stop()

    def count(self) -> int:
        """Return the number of registered modules."""

        return len(self._modules)