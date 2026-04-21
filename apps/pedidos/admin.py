from django.contrib import admin
from .models import Orden, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto', 'producto_nombre', 'tipo_venta', 'cantidad', 'precio_unitario']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'cliente_nombre', 'cliente_email', 'total', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion', 'region']
    search_fields = ['numero_orden', 'cliente_nombre', 'cliente_email', 'stripe_payment_intent']
    readonly_fields = ['numero_orden', 'stripe_payment_intent', 'fecha_creacion', 'fecha_actualizacion', 'fecha_pago']
    inlines = [DetallePedidoInline]
    list_editable = ['estado']
    fieldsets = (
        ('Identificación', {
            'fields': ('numero_orden', 'usuario', 'estado'),
        }),
        ('Cliente', {
            'fields': ('cliente_nombre', 'cliente_email', 'cliente_telefono'),
        }),
        ('Envío', {
            'fields': ('direccion', 'ciudad', 'region', 'codigo_postal', 'notas'),
        }),
        ('Pago', {
            'fields': ('total', 'stripe_payment_intent', 'fecha_pago'),
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )
