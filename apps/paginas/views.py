from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.productos.models import Producto
from .models import SugerenciaProducto, CATEGORIAS


def home(request):
    try:
        destacados = list(Producto.objects.filter(activo=True, destacado=True)[:4])
        if not destacados:
            destacados = list(Producto.objects.filter(activo=True).order_by('-creado')[:4])
    except Exception:
        destacados = []

    empresa_stats = {
        'anio_fundacion': getattr(settings, 'EMPRESA_ANIO_FUNDACION', None),
        'anios_herencia': getattr(settings, 'EMPRESA_ANIOS_HERENCIA', None),
        'n_marcas': getattr(settings, 'EMPRESA_N_MARCAS', None),
        'despacho_horas': getattr(settings, 'EMPRESA_DESPACHO_HORAS', None),
    }

    ya_participo = False
    if request.user.is_authenticated:
        ya_participo = SugerenciaProducto.objects.filter(usuario=request.user).exists()

    return render(request, 'paginas/home.html', {
        'destacados':   destacados,
        'stats':        empresa_stats,
        'categorias':   CATEGORIAS,
        'ya_participo': ya_participo,
    })


# ── Concurso sugerencia de producto ────────────────────────────────

@login_required
@require_POST
def sugerir_producto(request):
    if SugerenciaProducto.objects.filter(usuario=request.user).exists():
        messages.info(request, '¡Ya estás participando en el concurso!')
        return redirect('paginas:home')

    categoria = request.POST.get('categoria', '').strip()
    producto  = request.POST.get('producto', '').strip()
    categorias_validas = [c[0] for c in CATEGORIAS]

    if not categoria or categoria not in categorias_validas:
        messages.error(request, 'Selecciona una categoría válida.')
        return redirect('paginas:home')

    if not producto:
        messages.error(request, 'Escribe el nombre del producto que sugieres.')
        return redirect('paginas:home')

    SugerenciaProducto.objects.create(
        usuario=request.user,
        categoria=categoria,
        producto=producto,
    )

    messages.success(request, '¡Gracias por participar! Ya estás en el concurso.')
    return redirect('paginas:home')


# ── Validación de edad ──────────────────────────────────────────────

def _calcular_edad(nacimiento: date) -> int:
    hoy = date.today()
    years = hoy.year - nacimiento.year
    # Si aún no pasó el cumpleaños este año, restar 1
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        years -= 1
    return years


@require_http_methods(['GET', 'POST'])
def verificar_edad(request):
    """
    Gate de mayoría de edad:
      - Botón '+18' confirma acceso.
      - Botón '-18' redirige a acceso denegado.
    """
    ctx = {'edad_minima': settings.AGE_MINIMUM}

    if request.method == 'POST':
        if request.POST.get('edad') == 'menor':
            return redirect('paginas:acceso_denegado')

        # Cualquier otro valor (o 'mayor') da acceso
        request.session['edad_verificada'] = True
        response = redirect('paginas:home')
        response.set_signed_cookie(
            settings.AGE_VERIFICATION_COOKIE,
            'ok',
            max_age=settings.AGE_VERIFICATION_COOKIE_MAX_AGE,
            httponly=True,
            samesite='Lax',
            secure=not settings.DEBUG,
        )
        return response

    return render(request, 'paginas/verificar_edad.html', ctx)


def acceso_denegado(request):
    """Página informativa para quienes no cumplen la edad mínima."""
    return render(request, 'paginas/acceso_denegado.html', {
        'edad_minima': settings.AGE_MINIMUM,
    })


# ── Páginas informativas ────────────────────────────────────────────

def sobre_nosotros(request):
    return render(request, 'paginas/sobre_nosotros.html')


@require_http_methods(['GET', 'POST'])
def contacto(request):
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        email = (request.POST.get('email') or '').strip()
        mensaje = (request.POST.get('mensaje') or '').strip()

        if not (nombre and email and mensaje):
            messages.error(request, 'Po