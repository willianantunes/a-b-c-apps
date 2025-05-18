#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from letter_b.support.django_helpers import eval_env_as_boolean
from otlp import configure_opentelemetry


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "letter_b.settings")

    if eval_env_as_boolean("START_INSTRUMENT_ON_MANAGEPY", True):
        configure_opentelemetry()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
