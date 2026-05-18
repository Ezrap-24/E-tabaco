from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.productos.models import Producto


def home(request):
    try:
        # Prioriza los marcados como destacados; si no hay, muestra los 4 más recientes
        destacados = list(Producto.objects.filter(activo=True, destacado=True)[:4])
        if not destacados:
            destacados = list(Producto.objects.filter(activo=True).order_by('-creado')[:4])
    except Exception:
        destacados = []

    # ── Cifras del hero / stats ──
    # TODO(cliente): confirmar estas cifras con el dueño antes de publicar.
    # Se pueden sobreescribir en .env sin tocar el template.
    empresa_stats = {
        'anio_fundacion': getattr(settings, 'EMPRESA_ANIO_FUNDACION', None),
        'anios_herencia': getattr(settings, 'EMPRESA_ANIOS_HERENCIA', None),
        'n_marcas': getattr(settings, 'EMPRESA_N_MARCAS', None),
        'despacho_horas': getattr(settings, 'EMPRESA_DESPACHO_HORAS', None),
    }

    return render(request, 'paginas/home.html', {
        'destacados': destacados,
        'stats': empresa_stats,
    })


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
      - Pide fecha de nacimiento (día/mes/año).
      - Calcula edad real. Si >= AGE_MINIMUM, marca sesión
        y deposita una cookie firmada (30 días).
      - Si no cumple, redirige a /acceso-denegado/.
    """
    error = None

    ctx = {'error': None, 'edad_minima': settings.AGE_MINIMUM}

    if request.method == 'POST':
        try:
            dia = int(request.POST.get('dia', ''))
            mes = int(request.POST.get('mes', ''))
            anio = int(request.POST.get('anio', ''))
            nacimiento = date(anio, mes, dia)
        except (ValueError, TypeError):
            ctx['error'] = 'Ingresa una fecha de nacimiento válida.'
            return render(request, 'paginas/verificar_edad.html', ctx)

        if nacimiento > date.today():
            ctx['error'] = 'La fecha de nacimiento no puede ser futura.'
            return render(request, 'paginas/verificar_edad.html', ctx)

        edad = _calcular_edad(nacimiento)

        if edad < settings.AGE_MINIMUM:
            return redirect('paginas:acceso_denegado')

        # Verificación exitosa: sesión + cookie firmada persistente.
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
            messages.error(request, 'Por favor completa todos los campos.')
        else:
            cuerpo = (
                f'Nombre: {nombre}\n'
                f'Email: {email}\n\n'
                f'Mensaje:\n{mensaje}\n'
            )
            try:
                send_mail(
                    subject=f'[Contacto Puro Tabaco] {nombre}',
                    message=cuerpo,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'Recibimos tu mensaje. Te responderemos a la brevedad.',
                )
                return redirect('paginas:contacto')
            except Exception:
                messages.error(
                    request,
                    'No pudimos enviar el mensaje. Intenta nuevamente más tarde.',
                )

    return render(request, 'paginas/contacto.html')



def faqs(request):
    return render(request, 'paginas/faqs.html')


def terminos(request):
    return render(request, 'paginas/terminos.html')


def privacidad(request):
    return render(request, 'paginas/privacidad.html')
