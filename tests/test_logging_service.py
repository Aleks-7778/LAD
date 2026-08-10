"""Tests for LAD LoggingService."""

from pathlib import Path

from lad.config.settings import Settings
from lad.logging.service import LoggingService


def test_logging_service_creates_log_file(tmp_path: Path) -> None:
    log_file = tmp_path / "lad.log"
    settings = Settings(logging_file=str(log_file))

    service = LoggingService(settings)

    logger = service.get_logger()
    logger.info("test message")

    assert log_file.exists()
    assert "test message" in log_file.read_text(encoding="utf-8")

    service.shutdown()


def test_logging_service_returns_named_logger(tmp_path: Path) -> None:
    log_file = tmp_path / "lad.log"
    settings = Settings(logging_file=str(log_file))

    service = LoggingService(settings)

    logger = service.get_logger("core")

    assert logger.name == "lad.core"

    service.shutdown()


def test_logging_service_shutdown_removes_handlers(
    tmp_path: Path,
) -> None:
    log_file = tmp_path / "lad.log"
    settings = Settings(logging_file=str(log_file))

    service = LoggingService(settings)

    logger = service.get_logger()

    assert logger.handlers

    service.shutdown()

    assert service.logger.handlers == []
    assert service.configured is False


def test_logging_service_can_be_configured_again(
    tmp_path: Path,
) -> None:
    log_file = tmp_path / "lad.log"
    settings = Settings(logging_file=str(log_file))

    service = LoggingService(settings)

    service.configure()
    service.shutdown()
    service.configure()

    assert service.configured is True
    assert len(service.logger.handlers) == 1

    service.shutdown()


def test_application_registers_logging_service() -> None:
    from lad.core.application import Application

    app = Application()

    assert (
        app.service_container.resolve(LoggingService)
        is app.logging_service
    )
