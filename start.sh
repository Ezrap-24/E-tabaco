#!/bin/sh
set -e

echo ">>> Migraciones..."
python manage.py migrate --noinput

echo ">>> Cargando catálogo desde Excel..."
python manage.py cargar_catalogo || echo "Catálogo no cargado, se omite."

echo ">>> Colectando estáticos..."
python manage.py collectstatic --noinput

echo ">>> Iniciando servidor en puerto ${PORT:-8080}..."
gunicorn etabaco.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120
