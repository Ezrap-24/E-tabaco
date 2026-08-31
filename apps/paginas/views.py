import random
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.pedidos.models import DetallePedido
from apps.productos.models import Producto
from .models import SugerenciaProducto, CATEGORIAS

# Estados de orden que cuentan como venta real (excluye pendiente_pago y cancelado).
ESTADOS_VENTA_REAL = ('pagado', 'preparando', 'enviado', 'entregado')


def _mas_vendidos_con_marcas_variadas(cantidad=4):
    """Top productos por unidades vendidas (histórico completo), evitando
    repetir marca cuando hay suficiente variedad. Si no hay ventas registradas
    todavía, cae de vuelta al criterio anterior (destacado=True / más nuevos)."""
    ventas = (
        DetallePedido.objects
        .filter(orden__estado__in=ESTADOS_VENTA_REAL, producto__activo=True)
        .values('producto_id')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
    )
    ranking_ids = [v['producto_id'] for v in ventas]
    if not ranking_ids:
        return None  # sin ventas aún -> usar fallback

    productos_por_id = Producto.objects.in_bulk(ranking_ids)
    elegidos = []
    marcas_usadas = set()
    sobrantes = []

    for pid in ranking_ids:
        producto = productos_por_id.get(pid)
        if not producto:
            continue
        if producto.marca and producto.marca in marcas_usadas:
            sobrantes.append(producto)
            continue
        elegidos.append(producto)
        if producto.marca:
            marcas_usadas.add(producto.marca)
        if len(elegidos) >= cantidad:
            break

    if len(elegidos) < cantidad:
        for producto in sobrantes:
            if len(elegidos) >= cantidad:
                break
            elegidos.append(producto)

    return elegidos or None


def _marcas_disponibles():
    """Nombres de marca distintos con productos activos, para el listado/
    ticker de 'Nuestras marcas' del home. Deduplica variantes de mayusculas/
    minusculas del mismo nombre (ej. 'VERSO' y 'Verso' son la misma marca:
    se queda con la variante que tiene mas productos), sin tocar los datos
    en la base -- el filtro del catalogo (marca__iexact) ya matchea ambas."""
    filas = (
        Producto.objects.filter(activo=True)
        .exclude(marca='')
        .values('marca')
        .annotate(n=Count('id'))
    )
    por_clave = {}
    for fila in filas:
        clave = fila['marca'].strip().lower()
        if not clave:
            continue
        if clave not in por_clave or fila['n'] > por_clave[clave][1]:
            por_clave[clave] = (fila['marca'], fila['n'])
    return sorted((nombre for nombre, _n in por_clave.values()), key=str.lower)


def home(request):
    try:
        destacados = _mas_vendidos_con_marcas_variadas(4)
        if not destacados:
            destacados = list(Producto.objects.filter(activo=True, destacado=True)[:4])
        if not destacados:
            destacados = list(Producto.objects.filter(activo=True).order_by('-creado')[:4])
    except Exception:
        destacados = []

    try:
        franja_ids = list(
            Producto.objects.filter(activo=True).values_list('id', flat=True)
        )
        random.shuffle(franja_ids)
        franja_productos = list(Producto.objects.filter(id__in=franja_ids[:8]))
        # mantenemos el orden barajado (filter() no preserva el orden de la lista)
        orden_map = {pid: i for i, pid in enumerate(franja_ids[:8])}
        franja_productos.sort(key=lambda p: orden_map.get(p.id, 0))
    except Exception:
        franja_productos = []

    empresa_stats = {
        'anio_fundacion': getattr(settings, 'EMPRESA_ANIO_FUNDACION', None),
        'anios_herencia': getattr(settings, 'EMPRESA_ANIOS_HERENCIA', None),
        'n_marcas': getattr(settings, 'EMPRESA_N_MARCAS', None),
        'despacho_horas': getattr(settings, 'EMPRESA_DESPACHO_HORAS', None),
    }

    ya_participo = False
    if request.user.is_authenticated:
        ya_participo = SugerenciaProducto.objects.filter(usuario=request.user).exists()

    try:
        marcas_catalogo = _marcas_disponibles()
    except Exception:
        marcas_catalogo = []

    return render(request, 'paginas/home.html', {
        'destacados':       destacados,
        'franja_productos': franja_productos,
        'stats':            empresa_stats,
        'categorias':       CATEGORIAS,
        'ya_participo':     ya_participo,
        'marcas_catalogo':  marcas_catalogo,
    })


# ── Concurso sugerencia de producto ────────────────────────────────

@login_required
@require_POST
def sugerir_producto(request):
    if SugerenciaProducto.objects.filter(usuario=request.user).exists():
        messages.info(request, 'Ya estas participando en el concurso!')
        return redirect('paginas:home')

    categoria = request.POST.get('categoria', '').strip()
    producto  = request.POST.get('producto', '').strip()
    categorias_validas = [c[0] for c in CATEGORIAS]

    if not categoria or categoria not in categorias_validas:
        messages.error(request, 'Selecciona una categoria valida.')
        return redirect('paginas:home')

    if not producto:
        messages.error(request, 'Escribe el nombre del producto que sugieres.')
        return redirect('paginas:home')

    SugerenciaProducto.objects.create(
        usuario=request.user,
        categoria=categoria,
        producto=producto,
    )

    messages.success(request, 'Gracias por participar! Ya estas en el concurso.')
    return redirect('paginas:home')


# ── Validacion de edad ──────────────────────────────────────────────

def _calcular_edad(nacimiento: date) -> int:
    hoy = date.today()
    years = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        years -= 1
    return years


@require_http_methods(['GET', 'POST'])
def verificar_edad(request):
    ctx = {'edad_minima': settings.AGE_MINIMUM}

    if request.method == 'POST':
        if request.POST.get('edad') == 'menor':
            return redirect('paginas:acceso_denegado')

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
    return render(request, 'paginas/acceso_denegado.html', {
        'edad_minima': settings.AGE_MINIMUM,
    })


# ── Paginas informativas ────────────────────────────────────────────

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
            cuerpo = 'Nombre: {}\nEmail: {}\n\nMensaje:\n{}\n'.format(nombre, email, mensaje)
            try:
                send_mail(
                    subject='[Contacto Puro Tabaco] {}'.format(nombre),
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
                messages.error(request, 'Hubo un error al enviar tu mensaje. Intenta nuevamente.')

    return render(request, 'paginas/contacto.html')


def faq(request):
    return render(request, 'paginas/faqs.html')


def terminos(request):
    return render(request, 'paginas/terminos.html')


def privacidad(request):
    return render(request, 'paginas/privacidad.html')
