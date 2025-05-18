import logging
import os

from opentelemetry import metrics
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider

if os.getenv("OTEL_CUSTOM_EXPORTER_PROTOCOL", "grpc") == "grpc":
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
else:
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.propagate import inject
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry_instrumentation_django_stomp import DjangoStompInstrumentor


class OtelFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = getattr(record, "otelTraceID", None)
        if record.trace_id:
            del record.otelTraceID
        record.span_id = getattr(record, "otelSpanID", None)
        if record.span_id:
            del record.otelSpanID
        return True


def _response_hook(span, request, response):
    inject(response.headers)


# This is experimental and not recommended for production use.
# https://github.com/open-telemetry/opentelemetry-python/discussions/4294
class CustomLoggingHandler(LoggingHandler):
    def __init__(self, level=logging.NOTSET, logger_provider=None) -> None:
        logger_provider = LoggerProvider()
        set_logger_provider(logger_provider)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
        super().__init__(level, logger_provider)


def configure_opentelemetry():
    # https://opentelemetry-python.readthedocs.io/en/stable/exporter/otlp/otlp.html
    # Don't customize the provider, exporter, and so on programmatically. Use environment variables instead.
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    # TSHOOT PURPOSES ONLY: tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    # https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html#usage
    LoggingInstrumentor().instrument(tracer_provider=tracer_provider)
    DjangoInstrumentor().instrument(tracer_provider=tracer_provider, response_hook=_response_hook)
    # https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/psycopg/psycopg.html#module-opentelemetry.instrumentation.psycopg
    PsycopgInstrumentor().instrument(tracer_provider=tracer_provider, enable_commenter=True)
    URLLibInstrumentor().instrument(tracer_provider=tracer_provider)
    URLLib3Instrumentor().instrument(tracer_provider=tracer_provider)
    RequestsInstrumentor().instrument(tracer_provider=tracer_provider)
    DjangoStompInstrumentor().instrument(tracer_provider=tracer_provider)

    metrics.set_meter_provider(MeterProvider([PeriodicExportingMetricReader(OTLPMetricExporter())]))
    SystemMetricsInstrumentor().instrument()
