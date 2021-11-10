#!/bin/bash

echo '>> [Running] Django Collectstatic and Migrate'
python3 manage.py collectstatic --no-input &
python3 manage.py migrate --noinput &
# python3 manage.py run_celery_dev &
echo '>> [Running] Start Server'
gunicorn mis.wsgi:application --bind 0.0.0.0:80 --access-logfile '-' --error-logfile '-'
