from django.views.generic import ListView, DetailView
from .models import Producto, Categoria


class CatalogoView(ListView):
    model = Producto
    template_name = 'productos/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True)
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria_actual'] = self.request.GET.get('categoria')
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detalle.html'
    context_object_name = 'producto'

    def get_queryset(self):
        return Producto.objects.filter(activo=True)
