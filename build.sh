#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install

pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --no-input
pipenv run python manage.py add_superuser

celery --app team_production_system.tasks worker --loglevel info --concurrency 4
celery -A config.celery_settings beat -l debug

