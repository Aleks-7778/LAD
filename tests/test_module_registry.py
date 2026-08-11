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


class FailingModule:
    name = "failing"

    def __init__(self) -> None:
        self.started = False
        self.start_calls = 0
        self.stop_calls = 0

    def start(self) -> None:
        self.start_calls += 1
        raise RuntimeError("module startup failed")

    def stop(self) -> None:
        self.stop_calls += 1
        self.started = False


class TrackingModule:
    name = "tracking"

    def __init__(self) -> None:
        self.started = False
        self.start_calls = 0
        self.stop_calls = 0

    def start(self) -> None:
        self.start_calls += 1
        self.started = True

    def stop(self) -> None:
        self.stop_calls += 1
        self.started = False


def test_start_all_rolls_back_started_modules_on_failure() -> None:
    registry = ModuleRegistry()

    first = TrackingModule()
    failing = FailingModule()

    registry.register(first)
    registry.register(failing)

    try:
        registry.start_all()
        assert False, "Expected startup failure"
    except RuntimeError as exc:
        assert str(exc) == "module startup failed"

    assert first.started is False
    assert first.start_calls == 1
    assert first.stop_calls == 1

    assert failing.start_calls == 1
    assert failing.stop_calls == 0


def test_failed_start_does_not_leave_modules_marked_started() -> None:
    registry = ModuleRegistry()

    first = TrackingModule()
    failing = FailingModule()

    registry.register(first, name="first")
    registry.register(failing)

    try:
        registry.start_all()
    except RuntimeError:
        pass

    assert registry.start("first") is True
    assert first.start_calls == 2

    registry.stop("first")

    assert first.stop_calls == 2
