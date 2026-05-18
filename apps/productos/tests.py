import pytest
from django.urls import reverse
from apps.productos.models import Categoria, Producto


@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre='Tabaco Rubio')


@pytest.fixture
def producto(db, categoria):
    return Producto.objects.create(
        nombre='Virginia Gold',
        marca='Stanley',
        descripcion='Tabaco rubio suave de alta calidad.',
        precio_unidad=5.50,
        precio_mayor=4.50,
        cantidad_minima_mayor=3,
        stock=100,
        activo=True,
        categoria=categoria,
    )


def test_producto_str(producto):
    assert str(producto) == 'Stanley Virginia Gold'


def test_producto_tiene_stock(producto):
    assert producto.tiene_stock() is True


def test_producto_sin_stock(producto):
    producto.stock = 0
    assert producto.tiene_stock() is False


def test_catalogo_view(client, producto):
    url = reverse('productos:catalogo')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Virginia Gold' in response.content.decode()


def test_producto_detalle_view(client, producto):
    url = reverse('productos:detalle', kwargs={'pk': producto.pk})
    response = client.get(url)
    assert response.status_code == 200
