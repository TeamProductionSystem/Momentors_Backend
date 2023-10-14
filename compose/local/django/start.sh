#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Migrate database changes if necessary
python manage.py migrate

# Create superuser
python manage.py createsuperuser --no-input || true

# Finally, starts Django server
python manage.py runserver 0.0.0.0:8000