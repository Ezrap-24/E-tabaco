from django.conf import settings
from django.shortcuts import redirect

RUTAS_EXCLUIDAS = [
    '/verificar-edad/',
    '/health/',
    '/admin/',
    '/gestion-pt/',   # URL real del admin de Django
    '/pedidos/webhook/',
    '/pedidos/webpay/retorno/',
    '/static/',
    '/media/',
    '/cuenta/login/',
    '/cuenta/registro/',
    '/cuenta/password-reset/',
    '/acceso-denegado/',
    '/robots.txt',
    '/sitemap.xml',
    '/favicon.ico',
]

# Crawlers de buscadores: deben ver el contenido real (no el muro de edad)
# para poder indexar el sitio correctamente. Se les sirve el mismo contenido
# que ve un humano tras pasar el gate (no es cloaking penalizable).
BOTS_BUSCADORES = (
    'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider',
    'yandex', 'applebot', 'facebookexternalhit', 'twitterbot',
    'linkedinbot', 'whatsapp', 'google-inspectiontool',
)


def es_crawler(request):
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    return any(bot in ua for bot in BOTS_BUSCADORES)


class AgeVerificationMiddleware:
    """
    Gate de mayoria de edad.

    Orden de verificacion:
      1. Sesion (rapido, mismo navegador/tab).
      2. Cookie firmada persistente (30 dias por defecto).
         Si existe y es valida, rehidrata la sesion para evitar
         leer la cookie en cada request.
      3. Caso contrario, redirige al formulario de verificacion.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for ruta in RUTAS_EXCLUIDAS:
            if request.path.startswith(ruta):
                return self.get_response(request)

        # Dejar pasar a los crawlers de buscadores para que indexen el sitio.
        if es_crawler(request):
            return self.get_response(request)

        if request.session.get('edad_verificada'):
            return self.get_response(request)

        cookie_name = settings.AGE_VERIFICATION_COOKIE
        try:
            valor = request.get_signed_cookie(
                cookie_name,
                max_age=settings.AGE_VERIFICATION_COOKIE_MAX_AGE,
            )
        except Exception:
            valor = None

        if valor == 'ok':
            # Cookie valida: rehidrata la sesion y continua.
            request.session['edad_verificada'] = True
            return self.get_response(request)

        return redirect('paginas:verificar_edad')
