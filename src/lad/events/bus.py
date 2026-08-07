"""Event bus for LAD."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, Type


EventHandler = Callable[[Any], None]


class EventBus:
    """Simple in-process event bus."""

    def __init__(self) -> None:
        self._handlers: DefaultDict[
            Type[Any],
            list[EventHandler],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: Type[Any],
        handler: EventHandler,
    ) -> None:
        """Subscribe a handler to an event type."""

        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: Type[Any],
        handler: EventHandler,
    ) -> None:
        """Remove a handler from an event type."""

        handlers = self._handlers.get(event_type)

        if handlers is None:
            return

        if handler in handlers:
            handlers.remove(handler)

        if not handlers:
            self._handlers.pop(event_type, None)

    def publish(self, event: Any) -> None:
        """Publish an event to all subscribed handlers."""

        event_type = type(event)

        for handler in tuple(
            self._handlers.get(event_type, ())
        ):
            handler(event)

    def clear(self) -> None:
        """Remove all event subscriptions."""

        self._handlers.clear()

    def subscriber_count(
        self,
        event_type: Type[Any],
    ) -> int:
        """Return the number of subscribers for an event type."""

        return len(self._handlers.get(event_type, ()))