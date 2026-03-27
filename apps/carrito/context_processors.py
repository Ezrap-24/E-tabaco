from .carrito import Carrito


def carrito_context(request):
    """Hace el carrito disponible en todos los templates."""
    return {'carrito': Carrito(request)}
