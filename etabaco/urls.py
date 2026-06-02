from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse

def health(request):
    return HttpResponse('ok')

urlpatterns = [
    path('health/', health),
    path('gestion-pt/', admin.site.urls),
    path('', include('apps.paginas.urls')),
    path('catalogo/', include('apps.productos.urls')),
    path('carrito/', include('apps.carrito.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('cuenta/', include('apps.cuenta.urls')),
    # Servir media en producción (demo — reemplazar con S3 en producción real)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
