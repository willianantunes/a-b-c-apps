import os

from logging import Formatter
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

from pythonjsonlogger.jsonlogger import JsonFormatter

from letter_b.support.django_helpers import eval_env_as_boolean
from letter_b.support.django_helpers import getenv_or_raise_exception
from letter_b.support.django_helpers import strtobool

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "False"))

DJANGO_ALLOWED_HOSTS: Optional[str] = os.getenv("ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS:
    EXTRA_ALLOWED_HOST: Optional[str] = os.getenv("EXTRA_ALLOWED_HOST")
    FINAL_ALLOWED_HOSTS = f"{DJANGO_ALLOWED_HOSTS},{EXTRA_ALLOWED_HOST}" if EXTRA_ALLOWED_HOST else DJANGO_ALLOWED_HOSTS
    ALLOWED_HOSTS = FINAL_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS: Union[List[str], str]
if CSRF_TRUSTED_ORIGINS := os.getenv("CSRF_TRUSTED_ORIGINS", ""):
    CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS.split(",")

CSRF_COOKIE_SECURE = strtobool(os.getenv("CSRF_COOKIE_SECURE", "True"))
SESSION_COOKIE_SECURE = strtobool(os.getenv("SESSION_COOKIE_SECURE", "True"))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "request_id_django_log",
    "health_check",
    "health_check.db",
    "django_stomp",
    # Local apps
    "letter_b.apps.example",
]

MIDDLEWARE = [
    "letter_b.support.healthcheck.middlewares.LivenessHealthCheckMiddleware",
    "request_id_django_log.middleware.RequestIdDjangoLog",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "letter_b.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "letter_b.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 20)),
    "EXCEPTION_HANDLER": "letter_b.apps.example.api.global_exception_handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (),
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASE_CONN_MAX_AGE = int(os.getenv("DB_CONN_MAX_AGE", 0))
DATABASE_SSL_MODE = os.getenv("DB_SSL_MODE")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
        "OPTIONS": {"sslmode": DATABASE_SSL_MODE},
    }
}

if strtobool(os.getenv("DB_USE_REPLICA", "False")):
    DATABASES["replica"] = {
        "ENGINE": os.getenv("DB_REPLICA_ENGINE"),
        "NAME": os.getenv("DB_REPLICA_DATABASE"),
        "USER": os.getenv("DB_REPLICA_USER"),
        "HOST": os.getenv("DB_REPLICA_HOST"),
        "PORT": os.getenv("DB_REPLICA_PORT"),
        "PASSWORD": os.getenv("DB_REPLICA_PASSWORD"),
        "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
        "OPTIONS": {"sslmode": DATABASE_SSL_MODE},
    }
    DATABASE_ROUTERS: List[str] = [
        "letter_b.support.db_router.DatabaseRouter",
    ]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "request_id_django_log.filters.RequestIDFilter"},
        "redact_filter": {
            "()": "letter_b.support.logger.RedactingFilter",
            "patterns": ["cpf", "email", "birthday", "gender", "number", "emails", "username", "name", "phone"],
        },
    },
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        },
        "development": {
            "()": Formatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id", "redact_filter"],
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "letter_b": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {"level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.db.backends": {"level": os.getenv("DJANGO_DB_BACKENDS_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.request": {"level": os.getenv("DJANGO_REQUEST_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "stomp.py": {"level": os.getenv("STOMP_LOG_LEVEL", "WARNING"), "handlers": ["console"], "propagate": False},
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
USE_STATIC_FILE_HANDLER_FROM_WSGI = strtobool(os.getenv("USE_STATIC_FILE_HANDLER_FROM_WSGI", "true"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://github.com/juntossomosmais/request-id-django-log

REQUEST_ID_CONFIG = {
    "REQUEST_ID_HEADER": "HTTP_X_REQUEST_ID",
    "GENERATE_REQUEST_ID_IF_NOT_FOUND": True,
    "RESPONSE_HEADER_REQUEST_ID": "HTTP_X_REQUEST_ID",
}

HEALTH_CHECK = {
    "SUBSETS": {
        "integrations": [
            "DatabaseBackend",
            "DjangoSTOMPHealthCheck",
            "DjangoOutboxPatternHealthCheck",
        ],
        "readiness": [
            "CustomDatabaseBackendHealthCheck",
            "DjangoSTOMPHealthCheck",
            "DjangoOutboxPatternHealthCheck",
        ],
    },
}

# DEBUG CONFIGURATION
USE_DEBUG_APPS = eval_env_as_boolean("USE_DEBUG_APPS", False)
if DEBUG and USE_DEBUG_APPS:
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": (lambda request: True)}
    INTERNAL_IPS = ["0.0.0.0"]

    DEBUG_APPS = os.getenv("DEBUG_APPS")
    if DEBUG_APPS:
        INSTALLED_APPS += DEBUG_APPS.split(",")

    DEBUG_MIDDLEWARE = os.getenv("DEBUG_MIDDLEWARE")
    if DEBUG_MIDDLEWARE:
        MIDDLEWARE += DEBUG_MIDDLEWARE.split(",")

# STOMP
STOMP_LISTENER_CLIENT_ID = os.getenv("STOMP_LISTENER_CLIENT_ID")
STOMP_SERVER_HOST = os.getenv("STOMP_SERVER_HOST")
STOMP_SERVER_PORT = os.getenv("STOMP_SERVER_PORT")
STOMP_SERVER_STANDBY_HOST = os.getenv("STOMP_SERVER_STANDBY_HOST")
STOMP_SERVER_STANDBY_PORT = os.getenv("STOMP_SERVER_STANDBY_PORT")
STOMP_SERVER_USER = os.getenv("STOMP_SERVER_USER")
STOMP_SERVER_PASSWORD = os.getenv("STOMP_SERVER_PASSWORD")
STOMP_USE_SSL = eval_env_as_boolean("STOMP_USE_SSL", True)
STOMP_SERVER_VHOST = os.getenv("STOMP_SERVER_VHOST", "/")

# Broker
CREATE_AUDIT_ACTION_DESTINATION = os.getenv("CREATE_AUDIT_ACTION_DESTINATION", "/queue/create-audit-action")
