from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]
