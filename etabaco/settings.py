from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'django_htmx',
    # Apps propias
    'apps.productos',
    'apps.carrito',
    'apps.pedidos',
    'apps.paginas',
    'apps.cuenta',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    # Validación de edad — siempre al final
    'apps.paginas.middleware.AgeVerificationMiddleware',
]

ROOT_URLCONF = 'etabaco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Carrito disponible en todos los templates
                'apps.carrito.context_processors.carrito_context',
                # Datos de empresa (teléfono, email, envío gratis…)
                'apps.paginas.context_processors.empresa_context',
            ],
            'builtins': [
                'apps.paginas.templatetags.pt_filters',
            ],
        },
    },
]

WSGI_APPLICATION = 'etabaco.wsgi.application'

# Base de datos: DATABASE_URL en Railway, SQLite en desarrollo
_db_url = config('DATABASE_URL', default='')
if _db_url:
    DATABASES = {'default': dj_database_url.parse(_db_url, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Caché (memoria local del proceso) ───────────────────────
# Sin Redis disponible en el plan Hobby de Railway: usamos locmem.
# Reduce las consultas a Postgres por sesión en cada request.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'etabaco-cache',
    }
}

# Sesiones: lee/escribe en caché primero, cae a la base de datos solo
# si hay miss o restart del proceso. Evita el roundtrip a Postgres
# en cada visita (antes: backend 'db' puro, query en cada request).
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Localización Chile ──────────────────────────────────────
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Railway: dominios permitidos para CSRF
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000',
    cast=Csv(),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Autenticación ───────────────────────────────────────────
LOGIN_URL = 'cuenta:login'
LOGIN_REDIRECT_URL = 'cuenta:dashboard'
LOGOUT_REDIRECT_URL = 'paginas:home'

# ── Mercado Pago (moneda Chile: CLP) ────────────────────────
# Checkout Pro: el cliente paga en la página segura de Mercado Pago y vuelve.
# MP_ACCESS_TOKEN es la llave privada (servidor). Empieza con TEST- en pruebas.
MP_ACCESS_TOKEN = config('MP_ACCESS_TOKEN', default='')
MP_PUBLIC_KEY = config('MP_PUBLIC_KEY', default='')
MP_CURRENCY = config('MP_CURRENCY', default='CLP')

# URL pública del sitio, usada para construir back_urls y notification_url
# del checkout. En local apunta a tu túnel (ngrok) para que MP pueda avisar.
SITE_URL = config('SITE_URL', default='http://localhost:8000')

# ── Email (API HTTP de Resend) ──────────────────────────────
# Antes se mandaba por SMTP (smtp.resend.com:587), pero Railway bloquea las
# conexiones salientes por ese puerto — todo envío fallaba en silencio
# (TimeoutError atrapado por el try/except). La API HTTP (puerto 443) sí
# funciona. Dominio purotabaco.cl ya verificado en Resend (cuenta
# purotabacochile@gmail.com). Ver apps.pedidos.emailing.
#
# EMAIL_HOST_PASSWORD queda como fallback porque ahí ya estaba guardada la
# API key de Resend (variable histórica de la config SMTP anterior).
RESEND_API_KEY = config('RESEND_API_KEY', default=config('EMAIL_HOST_PASSWORD', default=''))
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='Puro Tabaco <noreply@purotabaco.cl>',
)
CONTACT_EMAIL = config('CONTACT_EMAIL', default='contacto@purotabaco.cl')

# Correo del negocio que recibe un aviso por cada venta concretada.
VENTAS_NOTIFY_EMAIL = config('VENTAS_NOTIFY_EMAIL', default='purotabacochile@gmail.com')

# ── Empresa (datos visibles en el sitio) ────────────────────
EMPRESA_TELEFONO = config('EMPRESA_TELEFONO', default='+56 9 1234 5678')
EMPRESA_TELEFONO_WSP = config('EMPRESA_TELEFONO_WSP', default='56912345678')
EMPRESA_EMAIL = config('EMPRESA_EMAIL', default='contacto@purotabaco.cl')

# ── Despacho (nunca es gratis) ──────────────────────────────
# Región Metropolitana: $2.500 fijo, se cobra dentro del pedido (Mercado Pago).
# Otras regiones: se despacha por Starken "por pagar" — el cliente paga al
# recibir, no se cobra nada por el sitio. Ver apps.pedidos.envio.

# ── Cifras del home (pendientes de validación con cliente) ──
# Dejar vacío/None mientras no estén confirmadas: el template las oculta.
def _int_or_none(key):
    raw = config(key, default='')
    raw = (raw or '').strip()
    try:
        return int(raw) if raw else None
    except (TypeError, ValueError):
        return None

EMPRESA_ANIO_FUNDACION = _int_or_none('EMPRESA_ANIO_FUNDACION')
EMPRESA_ANIOS_HERENCIA = _int_or_none('EMPRESA_ANIOS_HERENCIA')
EMPRESA_N_MARCAS = _int_or_none('EMPRESA_N_MARCAS')
EMPRESA_DESPACHO_HORAS = _int_or_none('EMPRESA_DESPACHO_HORAS')

# ── Validación de edad ──────────────────────────────────────
# Cookie firmada que recuerda la verificación (30 días por defecto).
AGE_VERIFICATION_COOKIE = 'edad_verificada'
AGE_VERIFICATION_COOKIE_MAX_AGE = config(
    'AGE_VERIFICATION_COOKIE_MAX_AGE',
    default=60 * 60 * 24 * 30,   # 30 días
    cast=int,
)
AGE_MINIMUM = config('AGE_MINIMUM', default=18, cast=int)

# ── Seguridad (solo prod) ───────────────────────────────────
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Railway termina TLS en su proxy — el redirect HTTPS lo maneja Railway/Cloudflare.
    # SECURE_SSL_REDIRECT queda desactivado para que el healthcheck interno (HTTP) no falle.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # HSTS: el navegador exige HTTPS por 1 año
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
