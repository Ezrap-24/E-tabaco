import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from apps.productos.models import Producto
from apps.carrito.carrito import Carrito


@pytest.fixture
def producto(db):
    return Producto.objects.create(
        nombre='Tabaco Negro',
        descripcion='Descripción test',
        precio_unidad=Decimal('6.00'),
        precio_caja=Decimal('50.00'),
        unidades_por_caja=10,
        stock=50,
        activo=True,
    )


@pytest.fixture
def request_con_sesion():
    factory = RequestFactory()
    request = factory.get('/')
    request.session = SessionStore()
    return request


def test_agregar_unidad_al_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=2, tipo_venta='unidad')
    assert carrito.cantidad_total() == 2
    assert carrito.cantidad_lineas() == 1


def test_agregar_caja_al_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=1, tipo_venta='caja')
    assert carrito.cantidad_total() == 1
    assert carrito.total() == Decimal('50.00')


def test_unidad_y_caja_son_lineas_separadas(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=2, tipo_venta='unidad')
    carrito.agregar(producto, cantidad=1, tipo_venta='caja')
    assert carrito.cantidad_lineas() == 2
    assert carrito.cantidad_total() == 3
    assert carrito.total() == Decimal('62.00')  # 2*6 + 1*50


def test_total_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=3, tipo_venta='unidad')
    assert carrito.total() == Decimal('18.00')


def test_eliminar_linea_especifica(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=2, tipo_venta='unidad')
    carrito.agregar(producto, cantidad=1, tipo_venta='caja')
    carrito.eliminar(producto.id, tipo_venta='unidad')
    assert carrito.cantidad_lineas() == 1
    assert carrito.cantidad_total() == 1


def test_carrito_vacio_tiene_total_cero(request_con_sesion):
    carrito = Carrito(request_con_sesion)
    assert carrito.total() == Decimal('0')
    assert len(carrito) == 0


def test_falta_envio_gratis(request_con_sesion, producto, settings):
    settings.ENVIO_GRATIS_DESDE = 100
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=5, tipo_venta='unidad')  # 30
    assert carrito.falta_envio_gratis() == Decimal('70')
    assert not carrito.califica_envio_gratis()
    carrito.agregar(producto, cantidad=2, tipo_venta='caja')  # +100
    assert carrito.falta_envio_gratis() == Decimal('0')
    assert carrito.califica_envio_gratis()
