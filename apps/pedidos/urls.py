from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('webhook/', views.mp_webhook, name='mp_webhook'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
    path('comprobante/<str:numero_orden>/', views.comprobante_pdf, name='comprobante_pdf'),
]
