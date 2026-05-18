from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from apps.productos.models import Producto
from .carrito import Carrito


def ver_carrito(request):
    return render(request, 'carrito/carrito.html', {'carrito': Carrito(request)})


def ver_drawer(request):
    """Devuelve solo el contenido del cart drawer (HTMX)."""
    return render(request, 'carrito/drawer_items.html', {'carrito': Carrito(request)})


@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (ValueError, TypeError):
        cantidad = 1
    tipo_venta = request.POST.get('tipo_venta', 'unidad')
    if tipo_venta not in ('unidad', 'caja'):
        tipo_venta = 'unidad'

    carrito.agregar(producto, cantidad=cantidad, tipo_venta=tipo_venta)

    if request.htmx:
        return render(request, 'carrito/agregar_confirmacion.html', {
            'producto': producto,
            'cantidad': cantidad,
            'tipo_venta': tipo_venta,
            'carrito': carrito,
            'carrito_total': carrito.cantidad_total(),
        })
    return redirect('carrito:ver')


@require_POST
def eliminar_del_carrito(request, producto_id, tipo_venta):
    carrito = Carrito(request)
    carrito.eliminar(producto_id, tipo_venta=tipo_venta)
    return _respuesta_carrito(request, carrito)


@require_POST
def actualizar_carrito(request, producto_id, tipo_venta):
    carrito = Carrito(request)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 1
    carrito.actualizar(producto_id, cantidad, tipo_venta=tipo_venta)
    return _respuesta_carrito(request, carrito)


def _respuesta_carrito(request, carrito):
    """Selecciona el template parcial correcto según el origen del request HTMX."""
    if request.htmx:
        target = request.headers.get('HX-Target', '')
        if 'cart-drawer-body' in target:
            return render(request, 'carrito/drawer_items.html', {'carrito': carrito})
        return render(request, 'carrito/carrito_fragment.html', {'carrito': carrito})
    return redirect('carrito:ver')
