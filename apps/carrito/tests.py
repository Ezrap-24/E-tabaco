import pytest
from django.test import RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from apps.productos.models import Producto
from apps.carrito.carrito import Carrito


@pytest.fixture
def producto(db):
    return Producto.objects.create(
        nombre='Tabaco Negro',
        descripcion='Descripción test',
        precio_unidad=6.00,
        precio_caja=50.00,
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


def test_agregar_caja_al_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=1, tipo_venta='caja')
    assert carrito.cantidad_total() == 1


def test_total_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=3, tipo_venta='unidad')
    assert carrito.total() == pytest.approx(18.00)


def test_eliminar_del_carrito(request_con_sesion, producto):
    carrito = Carrito(request_con_sesion)
    carrito.agregar(producto, cantidad=1, tipo_venta='unidad')
    carrito.eliminar(producto.id)
    assert carrito.cantidad_total() == 0


def test_carrito_vacio_tiene_total_cero(request_con_sesion):
    carrito = Carrito(request_con_sesion)
    assert carrito.total() == 0
