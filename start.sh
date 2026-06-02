#!/bin/sh
set -e

echo ">>> Migraciones..."
python manage.py migrate --noinput

echo ">>> Cargando datos iniciales..."
python manage.py loaddata fixtures/productos.json || echo "Fixture no encontrado, se omite."

echo ">>> Colectando estáticos..."
python manage.py collectstatic --noinput

echo ">>> Iniciando servidor en puerto ${PORT:-8080}..."
gunicorn etabaco.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120
