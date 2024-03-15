#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn --workers=1 --threads=2 setup.wsgi:application --bind 0.0.0.0:8000