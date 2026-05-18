"""
Django settings para desarrollo local (SQLite)
Importa de settings.py y sobrescribe DATABASES para usar SQLite
"""
from .settings import *

# Usar SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
