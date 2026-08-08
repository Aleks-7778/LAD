from __future__ import annotations

from lad.core.application import Application
from lad.events.application import (
    ApplicationStarted,
    ApplicationStarting,
    ApplicationStopped,
    ApplicationStopping,
)
from lad.events.bus import EventBus


def test_application_publishes_start_events() -> None:
    event_bus = EventBus()
    app = Application(event_bus=event_bus)

    received: list[object] = []

    event_bus.subscribe(
        ApplicationStarting,
        received.append,
    )
    event_bus.subscribe(
        ApplicationStarted,
        received.append,
    )

    app.initialize()
    app.start()

    assert len(received) == 2
    assert isinstance(received[0], ApplicationStarting)
    assert isinstance(received[1], ApplicationStarted)


def test_application_publishes_stop_events() -> None:
    event_bus = EventBus()
    app = Application(event_bus=event_bus)

    received: list[object] = []

    event_bus.subscribe(
        ApplicationStopping,
        received.append,
    )
    event_bus.subscribe(
        ApplicationStopped,
        received.append,
    )

    app.initialize()
    app.start()
    app.stop()

    assert len(received) == 2
    assert isinstance(received[0], ApplicationStopping)
    assert isinstance(received[1], ApplicationStopped)


def test_application_does_not_publish_start_events_twice() -> None:
    event_bus = EventBus()
    app = Application(event_bus=event_bus)

    received: list[object] = []

    event_bus.subscribe(
        ApplicationStarting,
        received.append,
    )
    event_bus.subscribe(
        ApplicationStarted,
        received.append,
    )

    app.initialize()
    app.start()
    app.start()

    assert len(received) == 2


def test_application_does_not_publish_stop_events_twice() -> None:
    event_bus = EventBus()
    app = Application(event_bus=event_bus)

    received: list[object] = []

    event_bus.subscribe(
        ApplicationStopping,
        received.append,
    )
    event_bus.subscribe(
        ApplicationStopped,
        received.append,
    )

    app.initialize()
    app.start()
    app.stop()
    app.stop()

    assert len(received) == 2
