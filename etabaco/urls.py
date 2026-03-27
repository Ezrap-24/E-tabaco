from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.paginas.urls')),
    path('catalogo/', include('apps.productos.urls')),
    path('carrito/', include('apps.carrito.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
