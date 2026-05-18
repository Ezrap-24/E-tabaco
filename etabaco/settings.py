from pathlib import Path
from decouple import config, Csv

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

# Usar SQLite en desarrollo, PostgreSQL en producción
# DEBUG se evalúa a partir de config('DEBUG') que lee del .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Autenticación ───────────────────────────────────────────
LOGIN_URL = 'cuenta:login'
LOGIN_REDIRECT_URL = 'cuenta:dashboard'
LOGOUT_REDIRECT_URL = 'paginas:home'

# ── Stripe (moneda Chile: CLP) ──────────────────────────────
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
STRIPE_CURRENCY = config('STRIPE_CURRENCY', default='clp')

# ── Email ───────────────────────────────────────────────────
# En desarrollo se imprime en consola; en producción usa SMTP.
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='Puro Tabaco <noreply@purotabaco.cl>',
)
CONTACT_EMAIL = config('CONTACT_EMAIL', default='contacto@purotabaco.cl')

# ── Empresa (datos visibles en el sitio) ────────────────────
EMPRESA_TELEFONO = config('EMPRESA_TELEFONO', default='+56 9 1234 5678')
EMPRESA_TELEFONO_WSP = config('EMPRESA_TELEFONO_WSP', default='56912345678')
EMPRESA_EMAIL = config('EMPRESA_EMAIL', default='contacto@purotabaco.cl')
ENVIO_GRATIS_DESDE = config('ENVIO_GRATIS_DESDE', default=50000, cast=int)

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
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
