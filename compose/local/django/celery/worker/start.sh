#!/bin/bash

set -o errexit
set -o nounset

celery -A config.celery worker -l INFO