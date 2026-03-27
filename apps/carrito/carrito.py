from decimal import Decimal
from apps.productos.models import Producto


class Carrito:
    """Maneja el carrito de compras almacenado en la sesión Django."""

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1, tipo_venta='unidad'):
        """Agrega un producto al carrito o actualiza su cantidad."""
        producto_id = str(producto.id)
        precio = float(producto.precio_unidad if tipo_venta == 'unidad' else producto.precio_caja)

        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'nombre': producto.nombre,
                'tipo_venta': tipo_venta,
                'cantidad': 0,
                'precio': precio,
            }

        # Si cambia el tipo de venta, resetear
        if self.carrito[producto_id]['tipo_venta'] != tipo_venta:
            self.carrito[producto_id]['tipo_venta'] = tipo_venta
            self.carrito[producto_id]['precio'] = precio
            self.carrito[producto_id]['cantidad'] = 0

        self.carrito[producto_id]['cantidad'] += cantidad
        self.guardar()

    def eliminar(self, producto_id):
        """Elimina un producto del carrito."""
        producto_id = str(producto_id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def actualizar(self, producto_id, cantidad):
        """Actualiza la cantidad de un producto."""
        producto_id = str(producto_id)
        if producto_id in self.carrito:
            if cantidad <= 0:
                self.eliminar(producto_id)
            else:
                self.carrito[producto_id]['cantidad'] = cantidad
                self.guardar()

    def guardar(self):
        """Marca la sesión como modificada para que Django la guarde."""
        self.session.modified = True

    def limpiar(self):
        """Vacía el carrito completo."""
        del self.session['carrito']
        self.guardar()

    def total(self):
        """Calcula el total del carrito."""
        return sum(
            Decimal(str(item['precio'])) * item['cantidad']
            for item in self.carrito.values()
        )

    def cantidad_total(self):
        """Retorna la cantidad total de items en el carrito."""
        return sum(item['cantidad'] for item in self.carrito.values())

    def items(self):
        """Retorna los items del carrito con objetos Producto."""
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carrito = self.carrito.copy()
        for producto in productos:
            carrito[str(producto.id)]['producto'] = producto
            carrito[str(producto.id)]['subtotal'] = (
                Decimal(str(carrito[str(producto.id)]['precio'])) *
                carrito[str(producto.id)]['cantidad']
            )
        return carrito.values()

    def __len__(self):
        return self.cantidad_total()
