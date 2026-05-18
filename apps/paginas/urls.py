from django.urls import path
from . import views

app_name = 'paginas'

urlpatterns = [
    path('', views.home, name='home'),
    path('verificar-edad/', views.verificar_edad, name='verificar_edad'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('faqs/', views.faqs, name='faqs'),
    path('terminos/', views.terminos, name='terminos'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
]
