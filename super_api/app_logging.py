import logging
from math import ceil as round_up
from time import time_ns
from typing import Optional

from flask import g, request
from flask.app import Flask
from flask.logging import default_handler
from pythonjsonlogger import jsonlogger

from super_api.config import settings

logger = logging.getLogger(__name__)


def _store_start_time():
    g.start_time = time_ns()


def _log_request_result(response):
    if request.path == "/health_check":
        return response
    data = {
        "status_code": response.status_code,
        "method": request.method,
        "path": request.path,
        "duration": f"{round_up((time_ns() - g.start_time) / 1_000_000)!s}ms",
        "query": request.query_string.decode("utf-8"),
        "user_agent": request.user_agent,
        "endpoint": request.endpoint,
        "scheme": request.scheme,
        "remote": request.remote_addr,
    }
    logger.info("Request complete", extra=data)
    return response


def configure_logging(
    app: Flask | None, package_name: Optional[str] = __package__
) -> None:
    """
    Configure a root logger.

    Behaviour depends on the `EXTRA_PYTHON_LOGGER_LEVEL` environment variable.

    :param app: The flask app to configure
    :type app: :py:class:`flask.Flask`
    :param package_name: The name of the package to configure. Should be `__package__`.
    :type package_name: str
    """
    root_logger = logging.getLogger(package_name)
    handler = default_handler
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(process)d"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(default_handler)

    root_logger.setLevel(settings.python_logger_level)

    if app:
        app.before_request(_store_start_time)
        app.after_request(_log_request_result)
