from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from apps.productos.models import Producto


def home(request):
    destacados = Producto.objects.filter(activo=True)[:4]
    return render(request, 'paginas/home.html', {'destacados': destacados})


@require_http_methods(['GET', 'POST'])
def verificar_edad(request):
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta == 'si':
            request.session['edad_verificada'] = True
            return redirect('paginas:home')
        else:
            return redirect('https://www.google.com')
    return render(request, 'paginas/verificar_edad.html')


def sobre_nosotros(request):
    return render(request, 'paginas/sobre_nosotros.html')


def contacto(request):
    enviado = False
    if request.method == 'POST':
        # En el MVP simplemente mostramos el mensaje de éxito
        enviado = True
    return render(request, 'paginas/contacto.html', {'enviado': enviado})


def faqs(request):
    return render(request, 'paginas/faqs.html')


def terminos(request):
    return render(request, 'paginas/terminos.html')


def privacidad(request):
    return render(request, 'paginas/privacidad.html')
