#!/usr/bin/env bash

set -e

python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py seed --create-super-user

gunicorn -cpython:gunicorn_config -b 0.0.0.0:${DJANGO_BIND_PORT:-8080} letter_b.wsgi
