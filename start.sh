#!/bin/sh
set -e

echo ">>> Migraciones..."
python manage.py migrate --noinput

echo ">>> Cargando datos iniciales..."
python manage.py loaddata fixtures/productos.json || echo "Fixture no encontrado, se omite."

echo ">>> Iniciando servidor..."
gunicorn etabaco.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
