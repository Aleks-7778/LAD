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


def test_application_initialize_is_idempotent() -> None:
    app = Application()

    app.initialize()
    first_settings = app.settings

    app.initialize()

    assert app.initialized is True
    assert app.settings is first_settings

    app.shutdown()


def test_application_start_is_idempotent() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.start()

    assert app.initialized is True
    assert app.running is True

    app.shutdown()


def test_application_stop_is_idempotent() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.stop()
    app.stop()

    assert app.initialized is True
    assert app.running is False

    app.shutdown()


def test_application_can_restart_after_stop() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.stop()
    app.start()

    assert app.initialized is True
    assert app.running is True

    app.shutdown()


def test_application_shutdown_is_idempotent() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.shutdown()
    app.shutdown()

    assert app.initialized is False
    assert app.running is False


def test_application_stop_does_not_uninitialize() -> None:
    app = Application()

    app.initialize()
    app.start()
    app.stop()

    assert app.initialized is True
    assert app.settings is not None

    app.shutdown()
