from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'ciudad', 'region')
    search_fields = ('usuario__email', 'usuario__first_name', 'ciudad')
