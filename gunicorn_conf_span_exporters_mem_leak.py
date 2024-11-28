import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

bind = "0.0.0.0:8080"
wsgi_app = "super_api.entrypoint_api"

worker_class = "gevent"
workers = 2
worker_connections = 1000
max_requests = 25
preload_app = False

errorlog = "-"

# Setup tracing
# https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model/README.html?highlight=gunicorn#working-with-fork-process-models
# https://docs.sentry.io/platforms/python/tracing/instrumentation/opentelemetry/
def post_fork(server, worker):
    resource = Resource.create({SERVICE_NAME: "super_api", "worker": worker.pid})
    tracer_provider = TracerProvider(resource=resource)

    otlp_endpoint = os.environ["TRACING_OTLP_ENDPOINT"]
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)


def post_worker_init(worker):
    import sentry_sdk
    from sentry_sdk.integrations.opentelemetry import (
        SentryPropagator,
        SentrySpanProcessor,
    )

    sentry_sdk.init(
        traces_sample_rate=1.0,
        instrumenter="otel",
    )

    # These are called multiple times on a single OTeL tracer, it doesn't look like it should work !
    tracer_provider = trace.get_tracer_provider()
    tracer_provider.add_span_processor(SentrySpanProcessor())
    set_global_textmap(SentryPropagator())
