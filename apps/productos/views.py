from django.views.generic import ListView, DetailView
from .models import Producto, Categoria


class CatalogoView(ListView):
    model = Producto
    template_name = 'productos/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True).exclude(imagen='').exclude(imagen=None)
        categoria_param = self.request.GET.get('categoria')
        if categoria_param:
            if categoria_param.isdigit():
                queryset = queryset.filter(categoria_id=categoria_param)
            else:
                queryset = queryset.filter(categoria__nombre__icontains=categoria_param)
        seccion_param = self.request.GET.get('seccion')
        if seccion_param:
            queryset = queryset.filter(seccion__iexact=seccion_param)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        marca = self.request.GET.get('marca')
        if marca:
            queryset = queryset.filter(marca__iexact=marca)
        peso = self.request.GET.get('peso')
        if peso and peso.isdigit():
            queryset = queryset.filter(peso_gramos=int(peso))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
        context['categorias'] = categorias

        # Filtros actuales
        categoria_param = self.request.GET.get('categoria', '')
        context['categoria_actual'] = categoria_param
        context['q_actual'] = self.request.GET.get('q', '')
        context['seccion_actual'] = self.request.GET.get('seccion', '')
        context['marca_actual'] = self.request.GET.get('marca', '')
        context['peso_actual'] = self.request.GET.get('peso', '')

        # Nombre legible de la categoria activa para el header
        categoria_nombre = ''
        if categoria_param:
            if categoria_param.isdigit():
                cat = categorias.filter(id=categoria_param).first()
                categoria_nombre = cat.nombre if cat else ''
            else:
                cat = categorias.filter(nombre__icontains=categoria_param).first()
                categoria_nombre = cat.nombre if cat else categoria_param.capitalize()
        context['categoria_nombre'] = categoria_nombre

        # Valores disponibles para los filtros (respetan la sección y categoría activa)
        qs_filtros = self.get_queryset()
        context['marcas_disponibles'] = (
            qs_filtros.exclude(marca='').values_list('marca', flat=True)
            .distinct().order_by('marca')
        )
        context['pesos_disponibles'] = (
            qs_filtros.exclude(peso_gramos=None).values_list('peso_gramos', flat=True)
            .distinct().order_by('peso_gramos')
        )

        # Preservar parametros GET para la paginacion (sin 'page')
        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_params'] = params.urlencode()
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detalle.html'
    context_object_name = 'producto'

    def get_queryset(self):
        return Producto.objects.filter(activo=True)
