#!/bin/sh
set -e

echo ">>> Migraciones..."
python manage.py migrate --noinput

# Carga el fixture SOLO si la base no tiene productos todavia (primer arranque).
# Asi los cambios hechos desde el admin (precios, stock, etc.) NO se sobrescriben
# en cada deploy.
echo ">>> Verificando datos iniciales..."
if python manage.py shell -c "import sys; from apps.productos.models import Producto; sys.exit(0 if Producto.objects.exists() else 1)"; then
    echo "    Ya hay productos en la base, no se recarga el fixture."
else
    echo "    Base vacia: cargando fixture inicial..."
    python manage.py loaddata fixtures/productos.json || echo "Fixture no encontrado, se omite."
fi

echo ">>> Colectando estáticos..."
python manage.py collectstatic --noinput

echo ">>> Iniciando servidor en puerto ${PORT:-8080}..."
gunicorn etabaco.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120
