from lad.core.application import Application
from lad.core.context import ApplicationContext


def test_context_available_after_initialize() -> None:
    app = Application()

    app.initialize()

    context = app.context

    assert isinstance(context, ApplicationContext)
    assert context.settings is app.settings
    assert context.container is app.service_container
    assert context.event_bus is app.event_bus
    assert context.module_registry is app.module_registry
    assert context.logging_service is app.logging_service
    assert context.sqlite_repository is app.sqlite_repository

    app.shutdown()


def test_context_requires_initialization() -> None:
    app = Application()

    try:
        app.context
        assert False, "context should require initialization"
    except RuntimeError as exc:
        assert str(exc) == "Application is not initialized"
    finally:
        app.shutdown()


def test_context_is_immutable() -> None:
    app = Application()
    app.initialize()

    context = app.context

    try:
        context.settings = context.settings
        assert False, "context should be immutable"
    except AttributeError:
        pass
    finally:
        app.shutdown()
