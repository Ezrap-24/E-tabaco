from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto


class ConFotoFilter(admin.SimpleListFilter):
    title = 'Foto'
    parameter_name = 'con_foto'

    def lookups(self, request, model_admin):
        return [
            ('si', 'Con foto'),
            ('no', 'Sin foto'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(imagen='').exclude(imagen=None)
        if self.value() == 'no':
            return queryset.filter(imagen='') | queryset.filter(imagen=None)
        return queryset


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'marca', 'categoria',
        'precio_unidad', 'precio_mayor',
        'stock', 'activo', 'destacado', 'tiene_foto',
    ]
    list_filter = ['activo', 'destacado', ConFotoFilter, 'categoria', 'marca', 'intensidad']
    search_fields = ['nombre', 'marca', 'codigo', 'descripcion']
    list_editable = ['activo', 'stock', 'destacado']

    @admin.display(description='Foto', boolean=True, ordering='imagen')
    def tiene_foto(self, obj):
        return bool(obj.imagen)
