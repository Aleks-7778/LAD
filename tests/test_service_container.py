from __future__ import annotations

import pytest

from lad.di.container import ServiceContainer


class TestService:
    pass


class AnotherService:
    pass


def test_container_can_register_and_resolve_service() -> None:
    container = ServiceContainer()

    service = TestService()
    container.register(TestService, service)

    assert container.resolve(TestService) is service


def test_container_returns_same_instance_for_registered_service() -> None:
    container = ServiceContainer()

    service = TestService()
    container.register(TestService, service)

    assert container.resolve(TestService) is service
    assert container.resolve(TestService) is service


def test_container_can_register_factory() -> None:
    container = ServiceContainer()

    container.register_factory(
        TestService,
        TestService,
    )

    first = container.resolve(TestService)
    second = container.resolve(TestService)

    assert isinstance(first, TestService)
    assert first is second


def test_container_reports_registered_service() -> None:
    container = ServiceContainer()

    service = TestService()
    container.register(TestService, service)

    assert container.is_registered(TestService)
    assert not container.is_registered(AnotherService)


def test_container_raises_for_unknown_service() -> None:
    container = ServiceContainer()

    with pytest.raises(KeyError):
        container.resolve(TestService)


def test_container_can_clear_services() -> None:
    container = ServiceContainer()

    container.register(TestService, TestService())

    assert container.is_registered(TestService)

    container.clear()

    assert not container.is_registered(TestService)
