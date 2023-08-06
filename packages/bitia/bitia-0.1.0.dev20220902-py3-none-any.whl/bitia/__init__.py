from importlib.metadata import version
import sentry_sdk
import os

import logging
from rich.logging import RichHandler
import logging.handlers

from sentry_sdk.integrations.logging import LoggingIntegration


__version__ = version("bitia")

log_level = os.environ.get("COPR_LOGLEVEL", "info").upper()
logging.basicConfig(
    format="%(message)s",
    level=log_level,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.WARNING,  # Send errors as events
)
sentry_sdk.init(
    dsn="https://176cf8fb9d1a4f53ac6af52049e9b102@traces.subcom.link/9",
    integrations=[
        sentry_logging,
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0.5,
)
