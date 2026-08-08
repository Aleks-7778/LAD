"""Dependency injection service container for LAD."""

from __future__ import annotations

from typing import Any, Callable, TypeVar


ServiceType = TypeVar("ServiceType")
Factory = Callable[[], Any]


class ServiceContainer:
    """Simple dependency injection container."""

    def __init__(self) -> None:
        self._services: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Factory] = {}

    def register(
        self,
        service_type: type[ServiceType],
        instance: ServiceType,
    ) -> None:
        """Register an existing service instance."""

        self._services[service_type] = instance
        self._factories.pop(service_type, None)

    def register_factory(
        self,
        service_type: type[ServiceType],
        factory: Callable[[], ServiceType],
    ) -> None:
        """Register a factory for a service."""

        self._factories[service_type] = factory
        self._services.pop(service_type, None)

    def resolve(
        self,
        service_type: type[ServiceType],
    ) -> ServiceType:
        """Resolve a registered service."""

        if service_type in self._services:
            return self._services[service_type]

        if service_type in self._factories:
            instance = self._factories[service_type]()
            self._services[service_type] = instance
            return instance

        raise KeyError(
            f"Service is not registered: {service_type!r}"
        )

    def is_registered(
        self,
        service_type: type[Any],
    ) -> bool:
        """Return True if a service is registered."""

        return (
            service_type in self._services
            or service_type in self._factories
        )

    def clear(self) -> None:
        """Remove all registered services and factories."""

        self._services.clear()
        self._factories.clear()
