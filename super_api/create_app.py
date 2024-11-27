"""
Provides a factory to create a :py:class:`flask.Flask` object with configured modules.

Configuration is provided through Dynaconf and also available in :py:mod:`super_api.config`
"""

import logging
import os

from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor

from super_api.app_logging import configure_logging
from super_api.config import settings

logger = logging.getLogger(__name__)


def create_app(
    *,
    name: str = "Extrality",
    package: str = __package__,
    **kwargs,
) -> Flask:
    """
    Creates a Flask app with configured database and commands.

    Args:
        name: Name of the app, defaults to Extrality
        package: Name of the package, for the logger configuration

    Returns:
        Preconfigured flask application
    """
    app = Flask(name, **kwargs)
    app.config["DEBUG"] = settings.debug
    app.config["TESTING"] = settings.testing
    configure_logging(app, package)

    if os.getenv("TRACING_OTLP_ENDPOINT"):
        FlaskInstrumentor().instrument_app(app)
        LoggingInstrumentor().instrument()
        URLLibInstrumentor().instrument()

    return app
