from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver'),
    path('drawer/', views.ver_drawer, name='drawer'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar'),
    path('actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar'),
]
