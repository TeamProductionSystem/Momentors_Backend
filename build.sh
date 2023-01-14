#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install

pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --no-input
pipenv run python manage.py add_superuser
