from lad.config.settings import Settings
from lad.core.application import Application
from lad.core.runtime import RuntimeContext


def test_runtime_context_is_available_after_initialize():
    app = Application()

    app.initialize()

    context = app.context

    assert isinstance(context, RuntimeContext)
    assert context.settings == app.settings
    assert context.services is app.service_container
    assert context.event_bus is app.event_bus
    assert context.module_registry is app.module_registry
    assert context.logging_service is app.logging_service
    assert context.sqlite_repository is app.sqlite_repository

    app.shutdown()


def test_runtime_context_exposes_logger():
    app = Application()

    app.initialize()

    context = app.context
    logger = context.get_logger("runtime-test")

    assert logger.name == "lad.runtime-test"

    app.shutdown()


def test_runtime_context_requires_initialized_application():
    app = Application()

    try:
        app.context
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert str(exc) == "Application is not initialized"


def test_runtime_context_contains_settings():
    app = Application()

    app.initialize()

    assert isinstance(app.context.settings, Settings)

    app.shutdown()
