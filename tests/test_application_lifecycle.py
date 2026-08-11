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


def test_application_start_initializes_automatically() -> None:
    app = Application()

    app.start()

    assert app.initialized is True
    assert app.running is True

    app.stop()


def test_application_initialize_is_idempotent() -> None:
    app = Application()

    app.initialize()
    first_settings = app.settings

    app.initialize()

    assert app.initialized is True
    assert app.settings is first_settings

    app.shutdown()


def test_application_shutdown_after_stop_is_idempotent() -> None:
    app = Application()

    app.start()
    app.stop()
    app.shutdown()
    app.shutdown()

    assert app.initialized is False
    assert app.running is False
