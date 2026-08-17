from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ContadorOrden, Orden, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto', 'producto_nombre', 'tipo_venta', 'cantidad', 'precio_unitario']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['folio_display', 'cliente_nombre', 'cliente_email', 'total', 'estado', 'fecha_creacion', 'descargar_link']
    list_filter = ['estado', 'fecha_creacion', 'region']
    search_fields = ['numero_orden', 'cliente_nombre', 'cliente_email', 'mp_payment_id', 'mp_preference_id']
    readonly_fields = ['folio_display', 'numero_orden', 'correlativo', 'mp_preference_id', 'mp_payment_id',
                       'fecha_creacion', 'fecha_actualizacion', 'fecha_pago', 'descargar_link']
    inlines = [DetallePedidoInline]

    def get_list_editable(self, request):
        # Vendedor no puede editar estado inline en el listado
        if request.user.groups.filter(name='Vendedor').exists() and not request.user.is_superuser:
            return []
        return ['estado']

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if request.user.groups.filter(name='Vendedor').exists() and not request.user.is_superuser:
            readonly += ['estado', 'usuario']
        return readonly

    fieldsets = (
        ('Identificación', {
            'fields': ('folio_display', 'numero_orden', 'correlativo', 'usuario', 'estado', 'descargar_link'),
        }),
        ('Cliente', {
            'fields': ('cliente_nombre', 'cliente_email', 'cliente_telefono'),
        }),
        ('Envío', {
            'fields': ('direccion', 'ciudad', 'region', 'codigo_postal', 'notas'),
        }),
        ('Pago', {
            'fields': ('costo_envio', 'total', 'mp_preference_id', 'mp_payment_id', 'fecha_pago'),
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Folio')
    def folio_display(self, obj):
        return obj.folio

    @admin.display(description='Comprobante')
    def descargar_link(self, obj):
        if obj.estado not in ('pagado', 'preparando', 'enviado', 'entregado'):
            return '—'
        url = reverse('pedidos:comprobante_pdf', args=[obj.numero_orden])
        return format_html(
            '<a href="{}" target="_blank" style="'
            'background:#30483A; color:#EFE6D6; padding:4px 10px; '
            'font-size:11px; text-decoration:none; letter-spacing:1px;">'
            '↓ PDF</a>',
            url
        )


@admin.register(ContadorOrden)
class ContadorOrdenAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ultimo']
    readonly_fields = ['ultimo']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
