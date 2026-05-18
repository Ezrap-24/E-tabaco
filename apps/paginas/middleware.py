from django.conf import settings
from django.shortcuts import redirect

RUTAS_EXCLUIDAS = [
    '/verificar-edad/',
    '/admin/',
    '/pedidos/webhook/',
    '/static/',
    '/media/',
    '/cuenta/login/',
    '/cuenta/registro/',
    '/cuenta/password-reset/',
    '/acceso-denegado/',
]


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
