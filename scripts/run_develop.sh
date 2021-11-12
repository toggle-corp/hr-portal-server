#!/bin/bash

# TODO: wait for database

python manage.py migrate --noinput
# python3 manage.py run_celery_dev &
python manage.py runserver 0.0.0.0:8050
