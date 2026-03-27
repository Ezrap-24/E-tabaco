from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio_unidad', 'precio_caja', 'stock', 'activo']
    list_filter = ['activo', 'categoria']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo', 'stock']
