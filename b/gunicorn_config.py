from gevent import monkey

# If you don't do this, you'll get the following error for example:
# DatabaseWrapper objects created in a thread can only be used in that same thread. The object with alias 'default' was created in thread id 140208374647872 and this is thread id 140208369922144
monkey.patch_all()

import json
import os

from pythonjsonlogger.jsonlogger import JsonFormatter

from gunicorn_custom_timeout import post_request_timeout
from gunicorn_custom_timeout import pre_request_timeout
from gunicorn_custom_timeout import worker_exit_timeout


def post_fork(server, worker):
    """
    https://opentelemetry-python.readthedocs.io/en/stable/examples/fork-process-model/README.html#gunicorn-post-fork-hook
    """
    from letter_b.support.django_helpers import eval_env_as_boolean

    if eval_env_as_boolean("START_INSTRUMENT_ON_GUNICORN_POST_FORK", True):
        server.log.info("Worker spawned (pid: %s) - starting instrumentation", worker.pid)
        from otlp import configure_opentelemetry

        configure_opentelemetry()
    else:
        server.log.info("Worker spawned (pid: %s) - skipping instrumentation", worker.pid)


bind = os.environ.get("DJANGO_BIND_ADDRESS", "0.0.0.0") + ":" + os.environ.get("DJANGO_BIND_PORT", "8000")
backlog = int(os.getenv("GUNICORN_BACKLOG", "2048"))
workers = int(os.getenv("GUNICORN_WORKERS", "3"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gevent")
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", "50"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "300"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "2"))
threads = int(os.getenv("GUNICORN_THREADS", "1"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "0"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "0"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))


class CustomJsonFormatter(JsonFormatter):
    def format(self, record):
        """Formats a log record and serializes to json"""
        try:
            if getattr(record, "otelSpanID", 0) != 0:
                del record.otelSpanID
            if getattr(record, "otelTraceID", 0) != 0:
                del record.otelTraceID
            record.msg = json.loads(record.getMessage())
        except json.JSONDecodeError:
            pass

        return super().format(record)


logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": CustomJsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "error_console": {"class": "logging.StreamHandler", "formatter": "standard"},
    },
    "loggers": {
        "gunicorn.error": {"handlers": ["error_console"], "level": "INFO", "propagate": False},
        "gunicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# Using `lower` because Gunicorn's documentation explicitly recommends it
# https://docs.gunicorn.org/en/stable/settings.html#access-log-format
ip_address_header = os.getenv("GUNICORN_IP_ADDRESS_HEADER", "x-original-forwarded-for").lower()
request_id_header = os.getenv("GUNICORN_REQUEST_ID_HEADER", "http_x_request_id").lower()
span_id = os.getenv("OPENTELEMETRY_SPANID_HEADER", "span_id").lower()
trace_id = os.getenv("OPENTELEMETRY_TRACEID_HEADER", "trace_id").lower()

errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
accesslog = "-"
access_log_format = (
    f'{{"message": "%(r)s", "request_id": "%({{{request_id_header}}}o)s", '
    f'"http_status": %(s)s, "ip_address": "%({{{ip_address_header}}}i)s", '
    f'"trace_id": "%({{{trace_id}}}o)s", "span_id": "%({{{span_id}}}o)s", '
    f'"response_length": "%(b)s", "referer": "%(f)s", "user_agent": "%(a)s", '
    f'"request_time": %(L)s, "date": "%(t)s"}}'
)

# The following adds a request timeout when using gevent workers
pre_request = pre_request_timeout
post_request = post_request_timeout
worker_exit = worker_exit_timeout
