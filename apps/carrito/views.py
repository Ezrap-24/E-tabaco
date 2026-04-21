from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from apps.productos.models import Producto
from .carrito import Carrito


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'carrito/carrito.html', {'carrito': carrito})


def ver_drawer(request):
    """Retorna solo el contenido del cart drawer (para HTMX)."""
    carrito = Carrito(request)
    return render(request, 'carrito/drawer_items.html', {'carrito': carrito})


@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    cantidad = int(request.POST.get('cantidad', 1))
    tipo_venta = request.POST.get('tipo_venta', 'unidad')
    carrito.agregar(producto, cantidad=cantidad, tipo_venta=tipo_venta)

    if request.htmx:
        return render(request, 'carrito/agregar_confirmacion.html', {
            'producto': producto,
            'cantidad': cantidad,
            'tipo_venta': tipo_venta,
            'carrito_total': carrito.cantidad_total(),
        })
    return redirect('carrito:ver')


@require_POST
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    carrito.eliminar(str(producto_id))

    if request.htmx:
        # Si viene del drawer usa el template del drawer, si no usa el fragment completo
        target = request.headers.get('HX-Target', '')
        if 'cart-drawer-body' in target:
            return render(request, 'carrito/drawer_items.html', {'carrito': carrito})
        return render(request, 'carrito/carrito_fragment.html', {'carrito': carrito})
    return redirect('carrito:ver')


@require_POST
def actualizar_carrito(request, producto_id):
    carrito = Carrito(request)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 1
    carrito.actualizar(str(producto_id), cantidad)

    if request.htmx:
        target = request.headers.get('HX-Target', '')
        if 'cart-drawer-body' in target:
            return render(request, 'carrito/drawer_items.html', {'carrito': carrito})
        return render(request, 'carrito/carrito_fragment.html', {'carrito': carrito})
    return redirect('carrito:ver')
