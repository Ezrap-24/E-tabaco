from django.urls import path
from . import views

app_name = 'cuenta'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('salir/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('direccion/', views.direccion, name='direccion'),
    path('detalles/', views.detalles, name='detalles'),
]
