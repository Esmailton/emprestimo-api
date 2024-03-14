#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
# DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput
echo "✅ Running tests.."
# pytest -v

python manage.py runserver 0.0.0.0:8000



# python manage.py createsuperuser --username jhon --email jhon@gmail.com