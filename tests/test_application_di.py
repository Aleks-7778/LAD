from __future__ import annotations

from lad.core.application import Application
from lad.di.container import ServiceContainer
from lad.events.bus import EventBus
from lad.modules.registry import ModuleRegistry


def test_application_accepts_service_container() -> None:
    container = ServiceContainer()

    app = Application(service_container=container)

    assert app.service_container is container


def test_application_registers_core_services_in_container() -> None:
    container = ServiceContainer()

    app = Application(service_container=container)

    assert container.resolve(EventBus) is app.event_bus
    assert container.resolve(ModuleRegistry) is app.module_registry


def test_application_creates_service_container_when_not_provided() -> None:
    app = Application()

    assert isinstance(app.service_container, ServiceContainer)


def test_application_exposes_registered_services() -> None:
    container = ServiceContainer()

    app = Application(service_container=container)

    assert app.service_container.resolve(EventBus) is app.event_bus
    assert app.service_container.resolve(ModuleRegistry) is app.module_registry
