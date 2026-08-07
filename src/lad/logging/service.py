from lad.logging.logger import create_logger


class LoggingService:
    """Logging Service."""

    def __init__(self):
        self.logger = create_logger()

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)