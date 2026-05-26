from django.contrib import admin
from .models import SugerenciaProducto


@admin.register(SugerenciaProducto)
class SugerenciaProductoAdmin(admin.ModelAdmin):
    list_display  = ('usuario', 'categoria', 'producto', 'creado')
    list_filter   = ('categoria',)
    search_fields = ('usuario__username', 'usuario__email', 'producto')
    readonly_fields = ('usuario', 'categoria', 'producto', 'creado')
    ordering      = ('-creado',)
