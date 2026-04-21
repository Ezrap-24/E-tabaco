# Plan de Migración: Monorepo con 3 Subproyectos Django

**Objetivo:** Convertir e-Tabaco en una arquitectura de monorepo donde:
- Código compartido vive en `shared/` (modelos, utils, componentes)
- 3 instancias Django independientes: `clubdeltabaco/`, `purotabaco/`, `zonatabaco/`
- Cada instancia tiene su propio settings.py, urls.py, static/, media/
- Se comparten apps generales (productos, carrito, pedidos) desde shared/

---

## Estructura Final

```
e-tabaco/
├── shared/                      # Código reutilizable por los 3 sitios
│   ├── apps/
│   │   ├── productos/          # Modelos de productos
│   │   ├── carrito/            # Lógica de carrito
│   │   ├── pedidos/            # Modelos de pedidos
│   │   └── paginas/            # Páginas comunes
│   ├── static/
│   │   ├── css/                # Estilos compartidos (Bootstrap)
│   │   └── js/                 # JS compartido
│   ├── templates/
│   │   ├── base.html           # Template base
│   │   └── components/         # Componentes reutilizables
│   └── utils/                  # Utilidades comunes
│
├── clubdeltabaco/              # Instancia 1: Club del Tabaco
│   ├── settings.py             # Config específica (DB, dominio, etc)
│   ├── urls.py                 # URLs específicas
│   ├── wsgi.py                 # WSGI específico
│   ├── static/
│   │   └── css/                # Estilos específicos de marca
│   ├── media/                  # Productos de Club del Tabaco
│   ├── templates/              # Templates específicos de marca
│   ├── fixtures/               # Data inicial
│   └── manage.py               # (opcional)
│
├── purotabaco/                 # Instancia 2: Puro Tabaco
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   ├── media/
│   ├── templates/
│   └── fixtures/
│
├── zonatabaco/                 # Instancia 3: Zona Tabaco
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   ├── media/
│   ├── templates/
│   └── fixtures/
│
├── manage.py                   # Script global (con DJANGO_SETTINGS_MODULE dinámico)
├── requirements.txt            # Deps comunes
├── docker-compose.yml          # 3 servicios Django
├── Dockerfile                  # Imagen base
└── .env                        # Vars globales (se pueden sobreescribir per-instancia)
```

---

## Paso 1: Crear estructura de directorios

```bash
# Crear carpetas principales
mkdir -p shared/apps shared/static shared/templates shared/utils
mkdir -p clubdeltabaco/{static,media,templates,fixtures}
mkdir -p purotabaco/{static,media,templates,fixtures}
mkdir -p zonatabaco/{static,media,templates,fixtures}
```

---

## Paso 2: Mover código a shared/

### Apps compartidas
```bash
# Mover apps a shared/
mv apps/productos shared/apps/
mv apps/carrito shared/apps/
mv apps/pedidos shared/apps/
mv apps/paginas shared/apps/
```

**Resultado:** `shared/apps/` contiene todas las apps reutilizables.

---

## Paso 3: Crear settings para cada instancia

Cada instancia tendrá su propio `settings.py`:

### clubdeltabaco/settings.py
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-clubdeltabaco')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['clubdeltabaco.cl', 'www.clubdeltabaco.cl', 'localhost']

SITE_ID = 1
BRAND_NAME = 'Club del Tabaco'
BRAND_SLUG = 'clubdeltabaco'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shared.apps.productos',
    'shared.apps.carrito',
    'shared.apps.pedidos',
    'shared.apps.paginas',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clubdeltabaco_db',
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'collected')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR.parent, 'shared', 'static'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR.parent, 'shared', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shared.context_processors.brand',
            ],
        },
    },
]

ROOT_URLCONF = 'clubdeltabaco.urls'
WSGI_APPLICATION = 'clubdeltabaco.wsgi.application'

# ... resto de settings ...
```

**Notas clave:**
- `BRAND_NAME`, `BRAND_SLUG` para identificar marca
- BD específica por instancia (`clubdeltabaco_db`, etc)
- STATIC/MEDIA directorios específicos
- TEMPLATES y STATIC_DIRS apuntan a compartido + específico

---

## Paso 4: URLs por instancia

### clubdeltabaco/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shared.apps.paginas.urls')),
    path('productos/', include('shared.apps.productos.urls')),
    path('carrito/', include('shared.apps.carrito.urls')),
    path('pedidos/', include('shared.apps.pedidos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Paso 5: manage.py global

### manage.py (raíz del proyecto)
```python
#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

def main():
    # Default: DJANGO_SETTINGS_MODULE = 'clubdeltabaco.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clubdeltabaco.settings')
    
    # Permitir override desde variable de entorno
    # export DJANGO_SETTINGS_MODULE=purotabaco.settings
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

**Uso:**
```bash
# Ejecutar commands para clubdeltabaco (default)
python manage.py runserver

# Ejecutar para purotabaco
export DJANGO_SETTINGS_MODULE=purotabaco.settings
python manage.py runserver 8001

# Ejecutar para zonatabaco
export DJANGO_SETTINGS_MODULE=zonatabaco.settings
python manage.py runserver 8002
```

---

## Paso 6: Docker & Deployment

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: tabaco_prod
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  clubdeltabaco:
    build: .
    command: bash -c "python manage.py migrate --settings=clubdeltabaco.settings && gunicorn clubdeltabaco.wsgi:application --bind 0.0.0.0:8000"
    environment:
      DJANGO_SETTINGS_MODULE: clubdeltabaco.settings
      DEBUG: "False"
      DB_HOST: db
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./clubdeltabaco/media:/app/clubdeltabaco/media
      - ./clubdeltabaco/static:/app/clubdeltabaco/static

  purotabaco:
    build: .
    command: bash -c "python manage.py migrate --settings=purotabaco.settings && gunicorn purotabaco.wsgi:application --bind 0.0.0.0:8001"
    environment:
      DJANGO_SETTINGS_MODULE: purotabaco.settings
      DEBUG: "False"
      DB_HOST: db
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    ports:
      - "8001:8001"
    depends_on:
      - db
    volumes:
      - ./purotabaco/media:/app/purotabaco/media
      - ./purotabaco/static:/app/purotabaco/static

  zonatabaco:
    build: .
    command: bash -c "python manage.py migrate --settings=zonatabaco.settings && gunicorn zonatabaco.wsgi:application --bind 0.0.0.0:8002"
    environment:
      DJANGO_SETTINGS_MODULE: zonatabaco.settings
      DEBUG: "False"
      DB_HOST: db
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    ports:
      - "8002:8002"
    depends_on:
      - db
    volumes:
      - ./zonatabaco/media:/app/zonatabaco/media
      - ./zonatabaco/static:/app/zonatabaco/static

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./clubdeltabaco/static:/app/clubdeltabaco/static
      - ./purotabaco/static:/app/purotabaco/static
      - ./zonatabaco/static:/app/zonatabaco/static
    depends_on:
      - clubdeltabaco
      - purotabaco
      - zonatabaco

volumes:
  postgres_data:
```

### nginx.conf (proxy reverso)
```nginx
upstream clubdeltabaco {
    server clubdeltabaco:8000;
}
upstream purotabaco {
    server purotabaco:8001;
}
upstream zonatabaco {
    server zonatabaco:8002;
}

server {
    listen 80;
    server_name clubdeltabaco.cl www.clubdeltabaco.cl;
    location / {
        proxy_pass http://clubdeltabaco;
    }
    location /static/ {
        alias /app/clubdeltabaco/static/;
    }
    location /media/ {
        alias /app/clubdeltabaco/media/;
    }
}

server {
    listen 80;
    server_name purotabaco.cl www.purotabaco.cl;
    location / {
        proxy_pass http://purotabaco;
    }
    location /static/ {
        alias /app/purotabaco/static/;
    }
    location /media/ {
        alias /app/purotabaco/media/;
    }
}

server {
    listen 80;
    server_name zonatabaco.cl www.zonatabaco.cl;
    location / {
        proxy_pass http://zonatabaco;
    }
    location /static/ {
        alias /app/zonatabaco/static/;
    }
    location /media/ {
        alias /app/zonatabaco/media/;
    }
}
```

---

## Ventajas de esta estructura

| Aspecto | Beneficio |
|--------|-----------|
| **Compartición** | Modelos, lógica, componentes comunes en `shared/` |
| **Independencia** | Cada sitio tiene settings, urls, static, media propios |
| **Escalabilidad** | Fácil agregar una 4ª marca sin duplicación |
| **Mantenimiento** | Bug en `shared/` → se arregla una vez para los 3 |
| **Flexibilidad** | Cada marca puede tener su propia BD, configuración, features |
| **Deploy** | 1 repositorio, 3 servicios Docker, 1 nginx |

---

## Checklist de migración

- [ ] Crear estructura de directorios
- [ ] Mover apps a shared/
- [ ] Crear settings para cada instancia
- [ ] Crear urls.py para cada instancia
- [ ] Crear wsgi.py para cada instancia
- [ ] Actualizar manage.py
- [ ] Actualizar requirements.txt
- [ ] Crear docker-compose.yml con 3 servicios
- [ ] Crear nginx.conf para routing
- [ ] Probar que cada sitio corre en puerto diferente
- [ ] Validar que se comparte base de datos correctamente
- [ ] Documentar convenciones para nuevas features
