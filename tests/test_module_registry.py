from __future__ import annotations

from dataclasses import dataclass

import pytest

from lad.modules.registry import ModuleRegistry


@dataclass
class FakeModule:
    name: str
    started: int = 0
    stopped: int = 0

    def start(self) -> None:
        self.started += 1

    def stop(self) -> None:
        self.stopped += 1


def test_module_registry_registers_module() -> None:
    registry = ModuleRegistry()

    module = FakeModule("test")

    registry.register(module)

    assert registry.count == 1
    assert registry.get("test") is module


def test_module_registry_prevents_duplicate_registration() -> None:
    registry = ModuleRegistry()

    first = FakeModule("test")
    second = FakeModule("test")

    registry.register(first)

    with pytest.raises(ValueError):
        registry.register(second)

    assert registry.count == 1
    assert registry.get("test") is first


def test_module_registry_starts_all_modules() -> None:
    registry = ModuleRegistry()

    first = FakeModule("first")
    second = FakeModule("second")

    registry.register(first)
    registry.register(second)

    registry.start_all()

    assert first.started == 1
    assert second.started == 1


def test_module_registry_stops_all_modules() -> None:
    registry = ModuleRegistry()

    first = FakeModule("first")
    second = FakeModule("second")

    registry.register(first)
    registry.register(second)

    registry.start_all()
    registry.stop_all()

    assert first.stopped == 1
    assert second.stopped == 1


def test_module_registry_does_not_start_module_twice() -> None:
    registry = ModuleRegistry()

    module = FakeModule("test")

    registry.register(module)

    registry.start_all()
    registry.start_all()

    assert module.started == 1


def test_module_registry_does_not_stop_module_twice() -> None:
    registry = ModuleRegistry()

    module = FakeModule("test")

    registry.register(module)

    registry.start_all()
    registry.stop_all()
    registry.stop_all()

    assert module.stopped == 1
