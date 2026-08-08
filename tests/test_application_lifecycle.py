from __future__ import annotations

from lad.core.application import Application


def test_application_can_be_initialized() -> None:
    app = Application()

    app.initialize()

    assert app.initialized is True


def test_application_starts_after_initialization() -> None:
    app = Application()

    app.initialize()
    app.start()

    assert app.initialized is True
    assert app.running is True


def test_application_stops() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.stop()

    assert app.running is False


def test_application_shutdown() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.stop()
    app.shutdown()

    assert app.initialized is False
    assert app.running is False
