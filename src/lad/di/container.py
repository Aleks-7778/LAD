class Container:
    """Dependency Injection Container."""

    def __init__(self):
        self._services = {}

    def register(self, cls):
        """Register service."""

        self._services[cls] = cls()

    def resolve(self, cls):
        """Resolve service."""

        return self._services[cls]