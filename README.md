# E-Tabaco Monorepo — Arquitectura Multi-Tienda

**Proyecto:** 3 ecommerces independientes en un monorepo Django  
**Dominios:** purotabaco.cl, clubdeltabaco.cl, zonatabaco.cl  
**Stack:** Django 4.2 + PostgreSQL + Bootstrap 5 + JavaScript  
**Deployment:** Docker + Nginx  

---

## 📁 Estructura del Proyecto

```
e-tabaco/
├── shared/                          # Código compartido (utils, base templates)
│   ├── apps/
│   │   ├── productos/               # App de productos
│   │   ├── carrito/                 # Lógica de carrito
│   │   ├── pedidos/                 # Gestión de pedidos
│   │   ├── paginas/                 # Páginas estáticas
│   │   └── usuarios/                # Autenticación
│   ├── static/
│   │   ├── css/                     # Bootstrap, estilos comunes
│   │   └── js/                      # JavaScript compartido
│   ├── templates/
│   │   ├── base.html                # Template base
│   │   └── components/              # Componentes reutilizables
│   └── utils/                       # Helpers, decorators, etc
│
├── purotabaco/                      # Instancia 1: Puro Tabaco
│   ├── settings.py                  # Config específica (BD, dominio, etc)
│   ├── urls.py                      # URLs
│   ├── wsgi.py                      # WSGI
│   ├── static/                      # Estilos y assets específicos
│   ├── media/                       # Fotos de productos
│   ├── templates/                   # Templates de marca
│   └── fixtures/                    # Data inicial
│
├── clubdeltabaco/                   # Instancia 2: Club del Tabaco
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   ├── media/
│   ├── templates/
│   └── fixtures/
│
├── zonatabaco/                      # Instancia 3: Zona Tabaco
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   ├── media/
│   ├── templates/
│   └── fixtures/
│
├── manage.py                        # Gestor Django global
├── requirements.txt                 # Dependencias Python
├── docker-compose.yml               # 3 servicios Django + DB + Nginx
├── Dockerfile                       # Imagen base
├── nginx.conf                       # Config proxy reverso
│
├── docs/
│   ├── PLAN-MIGRACION-MONOREPO.md      # Plan técnico detallado
│   ├── BRAND-GUIDE-PUROTABACO-v2.md    # Manual de marca (v2.0)
│   ├── FLUJO-CARRITO-CHECKOUT.md       # Flujo de compra
│   ├── NORMAS-VENTA-TABACO-CHILE.md    # Regulaciones legales
│   ├── DOCUMENTACION-COMPLETA.md       # Índice completo
│   │
│   └── design/                          # ✅ Diseño Canva (Nuevo)
│       ├── project/                     # Archivos exportados
│       │   ├── Puro Tabaco Landing.html # Archivo principal
│       │   ├── wireframes.html
│       │   └── design-canvas.jsx
│       └── IMPLEMENTACION-DESIGN.md     # Guía de integración
│
└── .env.example                     # Variables de entorno
```

---

## 🎨 Diseño Visual (COMPLETADO)

### Status: ✅ Diseño completado en Canva

**Archivos:**
- `docs/design/project/Puro Tabaco Landing.html` — Prototipo HTML/CSS/JS
- `docs/design/IMPLEMENTACION-DESIGN.md` — Guía de implementación

**Qué incluye:**
- ✅ Landing page completa
- ✅ Navegación responsive
- ✅ Colores exactos: Verde #30483A, Tan #C8B08A, Crema #EFE6D6
- ✅ Tipografía: Playfair Display + Lora
- ✅ Todas las secciones: Hero, Marcas, Ventajas, CTA, Footer
- ✅ Mobile-first responsive design

**Próximo paso:**
```bash
# 1. Leer la documentación
cat docs/design/IMPLEMENTACION-DESIGN.md

# 2. Implementar en Django templates
# 3. Crear static CSS/JS desde el HTML de Canva
```

---

## 🚀 Configuración Inicial

### 1. Clonar y setup

```bash
git clone <repo-url>
cd e-tabaco

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar .env
cp .env.example .env
```

### 2. Configurar base de datos

Cada instancia tiene su propia BD en PostgreSQL:

```bash
# Crear BDs en PostgreSQL
createdb purotabaco_db
createdb clubdeltabaco_db
createdb zonatabaco_db
```

---

## 🔧 Cómo trabajar en cada instancia

### Para **Puro Tabaco**:

```bash
# Migrations
export DJANGO_SETTINGS_MODULE=purotabaco.settings
python manage.py migrate

# Crear superuser
python manage.py createsuperuser --settings=purotabaco.settings

# Runserver
python manage.py runserver --settings=purotabaco.settings
# Accede a: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### Para **Club del Tabaco**:

```bash
export DJANGO_SETTINGS_MODULE=clubdeltabaco.settings
python manage.py runserver 8001 --settings=clubdeltabaco.settings
# Accede a: http://localhost:8001
```

### Para **Zona Tabaco**:

```bash
export DJANGO_SETTINGS_MODULE=zonatabaco.settings
python manage.py runserver 8002 --settings=zonatabaco.settings
# Accede a: http://localhost:8002
```

---

## 📊 Decisiones Arquitectónicas

| Aspecto | Decisión | Razón |
|--------|----------|-------|
| **Bases de datos** | 3 BDs separadas | Máxima independencia |
| **Usuarios** | Separados por marca | Cada tienda maneja su base de clientes |
| **Catálogo** | Cada marca tiene sus productos | Inventario independiente |
| **Código compartido** | En `shared/` | Reutilización de lógica, models, templates |
| **Static/Media** | Por instancia | Cada marca con su identidad visual |

---

## 📝 Convenciones de desarrollo

### Código compartido (shared/)

Si escribes código que usan **2 o más instancias**, va en `shared/`:
- Modelos base
- Utilidades
- Componentes de templates
- Middleware común

### Código específico de marca

Si es **solo para Puro Tabaco**, va en `purotabaco/`:
- Templates personalizados
- Estilos de marca
- Fixtures específicas
- Vistas custom

### Ejemplo: Agregar un modelo compartido

```python
# shared/apps/productos/models.py
class Producto(models.Model):
    marca = models.CharField(max_length=50)  # 'purotabaco', 'clubdeltabaco', 'zonatabaco'
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # ...
```

### Ejemplo: Template heredado

```django
{# purotabaco/templates/purotabaco/inicio.html #}
{% extends "base.html" %}
{% load static %}

{% block brand_css %}
    <link rel="stylesheet" href="{% static 'css/purotabaco-theme.css' %}">
{% endblock %}

{% block content %}
    <h1>Bienvenido a Puro Tabaco</h1>
    {# Contenido específico #}
{% endblock %}
```

---

## 🐳 Docker (Producción)

```bash
# Levantar todos los servicios
docker-compose up --build

# Ver logs
docker-compose logs -f purotabaco
docker-compose logs -f clubdeltabaco
docker-compose logs -f zonatabaco

# Acceder a cada sitio
# purotabaco.local
# clubdeltabaco.local
# zonatabaco.local
```

---

## 📚 Documentación

- `docs/PLAN-MIGRACION-MONOREPO.md` — Arquitectura técnica detallada
- `docs/BRAND-GUIDE-PUROTABACO.md` — Manual de marca para Puro Tabaco
- `docs/BRAND-GUIDE-CLUBDELTABACO.md` — Manual de marca para Club del Tabaco (próximo)
- `docs/BRAND-GUIDE-ZONATABACO.md` — Manual de marca para Zona Tabaco (próximo)

---

## 🔐 Variables de Entorno

Ver `.env.example` para lista completa:

```bash
# Global
DEBUG=False
SECRET_KEY=your-secret-key

# Database
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=postgres

# Puro Tabaco
PT_DB_NAME=purotabaco_db
PT_SECRET_KEY=purotabaco-secret-key

# Club del Tabaco
CT_DB_NAME=clubdeltabaco_db
CT_SECRET_KEY=clubdeltabaco-secret-key

# Zona Tabaco
ZT_DB_NAME=zonatabaco_db
ZT_SECRET_KEY=zonatabaco-secret-key
```

---

## 🚨 Troubleshooting

### Error: "No module named 'shared'"

```bash
# Verificar que PYTHONPATH incluye raíz del proyecto
export PYTHONPATH="${PYTHONPATH}:/ruta/a/e-tabaco"
python manage.py runserver --settings=purotabaco.settings
```

### Error: "Database does not exist"

```bash
# Asegúrate de crear la BD primero
createdb purotabaco_db

# Luego migraciones
python manage.py migrate --settings=purotabaco.settings
```

### Los estilos no se ven

```bash
# Recolectar static files
python manage.py collectstatic --settings=purotabaco.settings --noinput
```

---

## 📞 Soporte

Para dudas sobre:
- **Arquitectura:** ver `docs/PLAN-MIGRACION-MONOREPO.md`
- **Brand Puro Tabaco:** ver `docs/BRAND-GUIDE-PUROTABACO.md`
- **Nuevas features:** crear branch `feature/` y seguir convenciones

---

**Última actualización:** 2026-04-20  
**Versión:** 1.0
