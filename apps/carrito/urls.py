from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver'),
    path('drawer/', views.ver_drawer, name='drawer'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('eliminar/<int:producto_id>/<str:tipo_venta>/', views.eliminar_del_carrito, name='eliminar'),
    path('actualizar/<int:producto_id>/<str:tipo_venta>/', views.actualizar_carrito, name='actualizar'),
]
