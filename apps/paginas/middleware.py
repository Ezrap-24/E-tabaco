from django.shortcuts import redirect

RUTAS_EXCLUIDAS = [
    '/verificar-edad/',
    '/admin/',
    '/pedidos/webhook/',
    '/static/',
    '/media/',
    '/cuenta/login/',
    '/cuenta/registro/',
]


class AgeVerificationMiddleware:
    """Redirige a verificación de edad si el usuario no ha confirmado ser mayor."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Saltar rutas excluidas
        for ruta in RUTAS_EXCLUIDAS:
            if request.path.startswith(ruta):
                return self.get_response(request)

        # Si ya verificó, continuar normalmente
        if request.session.get('edad_verificada'):
            return self.get_response(request)

        # Si no verificó, redirigir al modal de verificación
        return redirect('paginas:verificar_edad')
