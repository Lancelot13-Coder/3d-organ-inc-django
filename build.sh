#!/usr/bin/env bash
# Se ejecuta en Render en cada despliegue
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
