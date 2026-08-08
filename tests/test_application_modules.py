from __future__ import annotations

from dataclasses import dataclass

from lad.core.application import Application
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


def test_application_starts_registered_modules() -> None:
    registry = ModuleRegistry()
    module = FakeModule("test")

    registry.register(module)

    app = Application(module_registry=registry)

    app.initialize()
    app.start()

    assert module.started == 1


def test_application_stops_registered_modules() -> None:
    registry = ModuleRegistry()
    module = FakeModule("test")

    registry.register(module)

    app = Application(module_registry=registry)

    app.initialize()
    app.start()
    app.stop()

    assert module.stopped == 1


def test_application_does_not_start_modules_twice() -> None:
    registry = ModuleRegistry()
    module = FakeModule("test")

    registry.register(module)

    app = Application(module_registry=registry)

    app.initialize()
    app.start()
    app.start()

    assert module.started == 1


def test_application_does_not_stop_modules_twice() -> None:
    registry = ModuleRegistry()
    module = FakeModule("test")

    registry.register(module)

    app = Application(module_registry=registry)

    app.initialize()
    app.start()
    app.stop()
    app.stop()

    assert module.stopped == 1
