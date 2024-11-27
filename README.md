```sh
# This one continuously does `add_span_processor`
TRACING_OTLP_ENDPOINT=127.0.0.1:999 SENTRY_DSN=http://example.com uv run gunicorn -c ./gunicorn_conf_span_exporters_mem_leak.py

# This one breaks after a few requests, it gets stuck on:
# Transient error StatusCode.UNAVAILABLE encountered while exporting traces to 127.0.0.1:999, retrying in 32s.
TRACING_OTLP_ENDPOINT=127.0.0.1:999 SENTRY_DSN=http://example.com uv run gunicorn -c ./gunicorn_conf_broken_otel_exporter.py
```
