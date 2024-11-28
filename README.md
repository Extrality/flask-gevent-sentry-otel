```sh
export TRACING_OTLP_ENDPOINT=http://127.0.0.1:999
export SENTRY_DSN=https://ee4daf4a0a89f468c9892dc01d11c2111@o411113.ingest.sentry.io/4111111111119743

# This one continuously does `add_span_processor`
uv run gunicorn -c ./gunicorn_conf_span_exporters_mem_leak.py

# This one breaks after a few requests, it gets stuck on:
# Transient error StatusCode.UNAVAILABLE encountered while exporting traces to 127.0.0.1:999, retrying in 32s.
uv run gunicorn -c ./gunicorn_conf_broken_otel_exporter.py

# This one uses HTTP which raises more often (breaks out of the exponential backoff logic)
uv run gunicorn -c gunicorn_conf_otel_http.py
```
