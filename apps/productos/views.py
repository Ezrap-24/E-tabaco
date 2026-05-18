from django.db.models import F
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
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        oferta = self.request.GET.get('oferta')
        if oferta:
            queryset = queryset.filter(precio_mayor__lt=F('precio_unidad'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
        context['categorias'] = categorias
        categoria_param = self.request.GET.get('categoria', '')
        context['categoria_actual'] = categoria_param
        context['q_actual'] = self.request.GET.get('q', '')
        context['oferta_activa'] = bool(self.request.GET.get('oferta'))

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
