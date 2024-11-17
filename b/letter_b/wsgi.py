import os

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "letter_b.settings")

wsgi_application = OpenTelemetryMiddleware(get_wsgi_application())

if settings.USE_STATIC_FILE_HANDLER_FROM_WSGI:
    application = StaticFilesHandler(wsgi_application)
else:
    application = wsgi_application
