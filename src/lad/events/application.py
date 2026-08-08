"""Application lifecycle events for LAD."""

from __future__ import annotations


class ApplicationStarting:
    """Published immediately before the application starts."""


class ApplicationStarted:
    """Published after the application has successfully started."""


class ApplicationStopping:
    """Published immediately before the application stops."""


class ApplicationStopped:
    """Published after the application has successfully stopped."""