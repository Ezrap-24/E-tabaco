from django.contrib.auth import views as auth_views
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

    # Recuperacion de contrasena (vistas built-in de Django)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='cuenta/password_reset_form.html',
             email_template_name='cuenta/email/password_reset_email.txt',
             subject_template_name='cuenta/email/password_reset_subject.txt',
             success_url='/cuenta/password-reset/enviado/',
         ),
         name='password_reset'),
    path('password-reset/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='cuenta/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='cuenta/password_reset_confirm.html',
             success_url='/cuenta/password-reset/listo/',
         ),
         name='password_reset_confirm'),
    path('password-reset/listo/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='cuenta/password_reset_complete.html',
         ),
         name='password_reset_complete'),
]
