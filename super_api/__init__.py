from importlib.metadata import version  # E402

from opentelemetry import trace  # E402

__version__ = version(__package__)
tracer = trace.get_tracer(__package__)
