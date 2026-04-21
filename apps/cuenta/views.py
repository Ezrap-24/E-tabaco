from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.pedidos.models import Orden
from .models import PerfilUsuario
from .forms import (
    LoginForm, RegistroForm, DireccionForm,
    DetallesCuentaForm, CambioPasswordForm
)


def get_or_create_perfil(user):
    """Obtiene o crea el perfil del usuario — necesario para usuarios previos a la migración."""
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
    return perfil


# ── Autenticación ──────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('cuenta:dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'cuenta:dashboard')
            return redirect(next_url)
        else:
            form.add_error(None, 'Correo o contraseña incorrectos.')

    return render(request, 'cuenta/login.html', {'form': form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('cuenta:dashboard')

    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'¡Bienvenido, {user.first_name}! Tu cuenta fue creada.')
        return redirect('cuenta:dashboard')

    return render(request, 'cuenta/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('paginas:home')


# ── Área privada ──────────────────────────────────────────────────

@login_required(login_url='cuenta:login')
def dashboard(request):
    perfil = get_or_create_perfil(request.user)
    ordenes_recientes = Orden.objects.filter(
        cliente_email=request.user.email
    ).order_by('-fecha_creacion')[:5]
    return render(request, 'cuenta/dashboard.html', {
        'ordenes_recientes': ordenes_recientes,
        'perfil': perfil,
    })


@login_required(login_url='cuenta:login')
def mis_pedidos(request):
    ordenes = Orden.objects.filter(
        cliente_email=request.user.email
    ).prefetch_related('detalles__producto')
    return render(request, 'cuenta/mis_pedidos.html', {'ordenes': ordenes})


@login_required(login_url='cuenta:login')
def direccion(request):
    perfil = get_or_create_perfil(request.user)
    form = DireccionForm(request.POST or None, instance=perfil)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dirección actualizada correctamente.')
        return redirect('cuenta:direccion')

    return render(request, 'cuenta/direccion.html', {'form': form})


@login_required(login_url='cuenta:login')
def detalles(request):
    detalles_form = DetallesCuentaForm(
        request.POST or None, instance=request.user
    )
    password_form = CambioPasswordForm(
        user=request.user,
        data=request.POST or None
    )

    if request.method == 'POST':
        if 'guardar_detalles' in request.POST and detalles_form.is_valid():
            detalles_form.save()
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('cuenta:detalles')
        elif 'cambiar_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('cuenta:detalles')

    return render(request, 'cuenta/detalles.html', {
        'detalles_form': detalles_form,
        'password_form': password_form,
    })
