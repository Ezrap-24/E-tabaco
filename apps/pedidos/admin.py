from django.contrib import admin
from .models import Orden, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto', 'tipo_venta', 'cantidad', 'precio_unitario']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'cliente_nombre', 'cliente_email', 'total', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_orden', 'cliente_nombre', 'cliente_email']
    readonly_fields = ['numero_orden', 'stripe_payment_intent', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [DetallePedidoInline]
    list_editable = ['estado']
