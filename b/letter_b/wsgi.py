import os

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from letter_b.support.django_helpers import eval_env_as_boolean

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "letter_b.settings")

start_instrument_on_managepy = eval_env_as_boolean("START_INSTRUMENT_ON_MANAGEPY", True)
start_instrument_on_gunicorn = eval_env_as_boolean("START_INSTRUMENT_ON_GUNICORN_POST_FORK", True)
if start_instrument_on_managepy or start_instrument_on_gunicorn:
    from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

    wsgi_application = OpenTelemetryMiddleware(get_wsgi_application())
else:
    wsgi_application = get_wsgi_application()

if settings.USE_STATIC_FILE_HANDLER_FROM_WSGI:
    application = StaticFilesHandler(wsgi_application)
else:
    application = wsgi_application
