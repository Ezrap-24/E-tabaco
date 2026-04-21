from decimal import Decimal
from django.conf import settings
from apps.productos.models import Producto


class Carrito:
    """Maneja el carrito de compras almacenado en la sesión Django.

    Estructura interna:
        session['carrito'] = {
            'pid:tipo_venta': {
                'producto_id': int,
                'nombre': str,
                'tipo_venta': 'unidad' | 'caja',
                'cantidad': int,
                'precio': float,
            },
            ...
        }

    La clave compuesta `pid:tipo_venta` permite que un mismo producto exista
    como dos líneas distintas (ej. 2 unidades + 1 caja).
    """

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    # ── Helpers ────────────────────────────────────────────
    @staticmethod
    def _key(producto_id, tipo_venta):
        return f"{producto_id}:{tipo_venta}"

    # ── Operaciones ────────────────────────────────────────
    def agregar(self, producto, cantidad=1, tipo_venta='unidad'):
        """Agrega un producto al carrito. Unidad y caja son líneas separadas."""
        key = self._key(producto.id, tipo_venta)
        precio = float(producto.precio_unidad if tipo_venta == 'unidad' else producto.precio_caja)

        if key not in self.carrito:
            self.carrito[key] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'tipo_venta': tipo_venta,
                'cantidad': 0,
                'precio': precio,
            }

        self.carrito[key]['cantidad'] += cantidad
        self.guardar()

    def eliminar(self, producto_id, tipo_venta=None):
        """Elimina una línea del carrito.

        Si se pasa `tipo_venta`, elimina solo esa variante.
        Si no, elimina todas las variantes de ese producto.
        """
        if tipo_venta:
            self.carrito.pop(self._key(producto_id, tipo_venta), None)
        else:
            for key in [k for k in self.carrito if k.startswith(f"{producto_id}:")]:
                del self.carrito[key]
        self.guardar()

    def actualizar(self, producto_id, cantidad, tipo_venta='unidad'):
        """Actualiza la cantidad de una línea del carrito."""
        key = self._key(producto_id, tipo_venta)
        if key in self.carrito:
            if cantidad <= 0:
                del self.carrito[key]
            else:
                self.carrito[key]['cantidad'] = cantidad
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def limpiar(self):
        self.session['carrito'] = {}
        self.guardar()

    # ── Cálculos ───────────────────────────────────────────
    def total(self):
        """Total monetario del carrito."""
        return sum(
            (Decimal(str(item['precio'])) * item['cantidad']
             for item in self.carrito.values()),
            Decimal('0'),
        )

    def cantidad_total(self):
        """Suma de todas las unidades (lo que va en el badge)."""
        return sum(item['cantidad'] for item in self.carrito.values())

    def cantidad_lineas(self):
        """Número de líneas distintas (ej. para 'X productos')."""
        return len(self.carrito)

    def falta_envio_gratis(self):
        """Cuánto falta en pesos para alcanzar el envío gratis. 0 si ya califica."""
        umbral = Decimal(str(settings.ENVIO_GRATIS_DESDE))
        falta = umbral - self.total()
        return max(falta, Decimal('0'))

    def califica_envio_gratis(self):
        return self.total() >= Decimal(str(settings.ENVIO_GRATIS_DESDE))

    # ── Iteración ──────────────────────────────────────────
    def items(self):
        """Devuelve los items del carrito con su Producto asociado.
        Crea dicts nuevos para no contaminar la sesión.
        """
        producto_ids = {item['producto_id'] for item in self.carrito.values()}
        productos = Producto.objects.filter(id__in=producto_ids)
        productos_dict = {p.id: p for p in productos}

        items_lista = []
        for key, datos in self.carrito.items():
            producto = productos_dict.get(datos['producto_id'])
            if not producto:
                continue
            items_lista.append({
                'key':        key,
                'producto':   producto,
                'nombre':     datos['nombre'],
                'tipo_venta': datos['tipo_venta'],
                'cantidad':   datos['cantidad'],
                'precio':     Decimal(str(datos['precio'])),
                'subtotal':   Decimal(str(datos['precio'])) * datos['cantidad'],
            })
        return items_lista

    # `len(carrito)` y `carrito|length` devuelven la cantidad total de unidades
    # (consistente con el badge del icono).
    def __len__(self):
        return self.cantidad_total()
