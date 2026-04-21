from .carrito import Carrito


def carrito_context(request):
    """Hace el carrito disponible en todos los templates.

    Cachea la instancia en el request para no reconstruir el objeto
    en cada lookup del template.
    """
    if not hasattr(request, '_carrito'):
        request._carrito = Carrito(request)
    return {'carrito': request._carrito}
