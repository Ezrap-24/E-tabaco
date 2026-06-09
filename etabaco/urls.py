from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse, Http404
import os, re, mimetypes


def health(request):
    return HttpResponse('ok')


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


urlpatterns = [
    path('health/', health),
    path('gestion-pt/', admin.site.urls),
    path('', include('apps.paginas.urls')),
    path('catalogo/', include('apps.productos.urls')),
    path('carrito/', include('apps.carrito.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('cuenta/', include('apps.cuenta.urls')),
    re_path(r'^media/(?P<path>.*)$', serve_media),
]
