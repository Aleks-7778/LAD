"""Tests for LAD EventBus."""

from lad.events.bus import EventBus


class ApplicationStarted:
    """Test event."""

    def __init__(self, message: str) -> None:
        self.message = message


def test_event_bus_publish() -> None:
    """Event bus should deliver an event to subscribers."""

    bus = EventBus()
    received: list[ApplicationStarted] = []

    def handler(event: ApplicationStarted) -> None:
        received.append(event)

    bus.subscribe(ApplicationStarted, handler)

    event = ApplicationStarted("LAD started")

    bus.publish(event)

    assert received == [event]


def test_event_bus_unsubscribe() -> None:
    """Event bus should stop delivering events after unsubscribe."""

    bus = EventBus()
    received: list[ApplicationStarted] = []

    def handler(event: ApplicationStarted) -> None:
        received.append(event)

    bus.subscribe(ApplicationStarted, handler)
    bus.unsubscribe(ApplicationStarted, handler)

    bus.publish(ApplicationStarted("LAD started"))

    assert received == []


def test_event_bus_prevents_duplicate_subscription() -> None:
    """The same handler should not be registered twice."""

    bus = EventBus()

    def handler(event: ApplicationStarted) -> None:
        pass

    bus.subscribe(ApplicationStarted, handler)
    bus.subscribe(ApplicationStarted, handler)

    assert bus.subscriber_count(ApplicationStarted) == 1


def test_event_bus_clear() -> None:
    """Clear should remove all subscriptions."""

    bus = EventBus()

    def handler(event: ApplicationStarted) -> None:
        pass

    bus.subscribe(ApplicationStarted, handler)

    bus.clear()

    assert bus.subscriber_count(ApplicationStarted) == 0