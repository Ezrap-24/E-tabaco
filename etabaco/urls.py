from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse, Http404, HttpResponsePermanentRedirect
from urllib.parse import quote
import os, re, mimetypes


def health(request):
    return HttpResponse('ok')


def favicon_ico(request):
    from django.shortcuts import redirect
    from django.templatetags.static import static
    return redirect(static('img/favicon.png'), permanent=True)


def robots_txt(request):
    host = request.get_host()
    scheme = request.scheme
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /carrito/',
        'Disallow: /cuenta/',
        'Disallow: /gestion-pt/',
        'Disallow: /verificar-edad/',
        'Disallow: /catalogo/?',
        f'Sitemap: {scheme}://{host}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    from django.urls import reverse
    base = f'{request.scheme}://{request.get_host()}'
    paths = [
        reverse('paginas:home'),
        reverse('productos:catalogo'),
        reverse('paginas:sobre_nosotros'),
        reverse('paginas:contacto'),
        reverse('paginas:faqs'),
        reverse('paginas:terminos'),
        reverse('paginas:privacidad'),
    ]
    try:
        from apps.productos.models import Producto
        for pk in Producto.objects.filter(activo=True).values_list('pk', flat=True):
            paths.append(reverse('productos:detalle', args=[pk]))
    except Exception:
        pass

    urls = ''.join(f'<url><loc>{base}{p}</loc></url>' for p in paths)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'{urls}</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


def serve_media(request, path):
    """Sirve archivos de media con soporte de HTTP Range Requests (requerido por iOS Safari para video)."""
    # Protección contra path traversal: verificar que la ruta resuelta
    # esté dentro de MEDIA_ROOT antes de servir cualquier archivo.
    media_root = os.path.realpath(str(settings.MEDIA_ROOT))
    full_path = os.path.realpath(os.path.join(media_root, path))
    if not full_path.startswith(media_root + os.sep) and full_path != media_root:
        raise Http404
    if not os.path.exists(full_path):
        raise Http404

    file_size = os.path.getsize(full_path)
    content_type = mimetypes.guess_type(full_path)[0] or 'application/octet-stream'
    range_header = request.META.get('HTTP_RANGE', '').strip()

    def file_iterator(path, offset=0, length=None, chunk=8192):
        with open(path, 'rb') as f:
            f.seek(offset)
            remaining = length if length is not None else file_size - offset
            while remaining > 0:
                data = f.read(min(chunk, remaining))
                if not data:
                    break
                remaining -= len(data)
                yield data

    if range_header:
        m = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if m:
            first = int(m.group(1))
            last = int(m.group(2)) if m.group(2) else file_size - 1
            last = min(last, file_size - 1)
            length = last - first + 1
            response = StreamingHttpResponse(
                file_iterator(full_path, offset=first, length=length),
                status=206,
                content_type=content_type,
            )
            response['Content-Range'] = f'bytes {first}-{last}/{file_size}'
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = str(length)
            return response

    response = StreamingHttpResponse(file_iterator(full_path), content_type=content_type)
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(file_size)
    return response



# ── Redirecciones SEO: URLs heredadas de la plataforma anterior (WordPress/WooCommerce) ──
# Google todavía tiene indexadas estas rutas viejas, que hoy no existen y devuelven 404.
# Las redirigimos (301, permanente) a su equivalente real en el catalogo actual,
# en vez de dejarlas como enlaces muertos.

def redirect_producto_legacy(request, slug):
    return HttpResponsePermanentRedirect('/catalogo/')


def redirect_categoria_legacy(request, slug):
    texto = slug.rstrip('/').split('/')[-1].replace('-', ' ')
    return HttpResponsePermanentRedirect(f'/catalogo/?categoria={quote(texto)}')


def redirect_blog_legacy(request, slug=None):
    return HttpResponsePermanentRedirect('/')


urlpatterns = [
    path('health/', health),
    path('favicon.ico', favicon_ico),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap_xml),
    path('gestion-pt/', admin.site.urls),
    path('', include('apps.paginas.urls')),
    path('catalogo/', include('apps.productos.urls')),
    path('carrito/', include('apps.carrito.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('cuenta/', include('apps.cuenta.urls')),
    re_path(r'^producto/(?P<slug>[^/]+)/?$', redirect_producto_legacy),
    re_path(r'^categoria-producto/(?P<slug>.+)/?$', redirect_categoria_legacy),
    path('blog/', redirect_blog_legacy),
    re_path(r'^blog/(?P<slug>[^/]+)/?$', redirect_blog_legacy),
    re_path(r'^media/(?P<path>.*)$', serve_media),
]
