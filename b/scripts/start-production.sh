#!/usr/bin/env bash

set -e

python manage.py makemigrations --check --dry-run
python manage.py migrate

gunicorn -cpython:gunicorn_config -b 0.0.0.0:${DJANGO_BIND_PORT:-8080} letter_b.wsgi
