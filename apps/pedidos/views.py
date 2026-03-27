import stripe
import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from apps.carrito.carrito import Carrito
from .models import Orden, DetallePedido
from .forms import CheckoutForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    carrito = Carrito(request)
    if len(carrito) == 0:
        return redirect('carrito:ver')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Guardar datos del formulario en sesión para usarlos luego del pago
            request.session['checkout_data'] = form.cleaned_data
            # Crear PaymentIntent de Stripe
            total_centavos = int(carrito.total() * 100)
            intent = stripe.PaymentIntent.create(
                amount=total_centavos,
                currency='ars',  # Cambiar según el país
                metadata={'integration_check': 'accept_a_payment'},
            )
            return render(request, 'pedidos/checkout_pago.html', {
                'form': form,
                'carrito': carrito,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
            })
    else:
        form = CheckoutForm()

    return render(request, 'pedidos/checkout.html', {
        'form': form,
        'carrito': carrito,
    })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        _crear_orden_desde_pago(request, payment_intent)

    return HttpResponse(status=200)


def _crear_orden_desde_pago(request, payment_intent):
    """Crea la orden en la base de datos después de un pago exitoso."""
    checkout_data = request.session.get('checkout_data', {})
    carrito = Carrito(request)

    orden = Orden.objects.create(
        cliente_nombre=checkout_data.get('nombre', ''),
        cliente_email=checkout_data.get('email', ''),
        cliente_telefono=checkout_data.get('telefono', ''),
        direccion_envio=checkout_data.get('direccion', ''),
        total=carrito.total(),
        stripe_payment_intent=payment_intent['id'],
        estado='pagado',
    )

    for item in carrito.items():
        DetallePedido.objects.create(
            orden=orden,
            producto=item['producto'],
            tipo_venta=item['tipo_venta'],
            cantidad=item['cantidad'],
            precio_unitario=Decimal(str(item['precio'])),
        )

    carrito.limpiar()
    _enviar_email_confirmacion(orden)
    request.session['ultimo_numero_orden'] = orden.numero_orden


def _enviar_email_confirmacion(orden):
    """Envía el email de confirmación al cliente."""
    asunto = f'Confirmación de pedido {orden.numero_orden} — e-Tabaco'
    mensaje_html = render_to_string('email/confirmacion_pedido.html', {'orden': orden})
    send_mail(
        subject=asunto,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[orden.cliente_email],
        html_message=mensaje_html,
        fail_silently=True,
    )


def confirmacion(request):
    numero_orden = request.session.get('ultimo_numero_orden')
    if not numero_orden:
        return redirect('paginas:home')
    orden = get_object_or_404(Orden, numero_orden=numero_orden)
    return render(request, 'pedidos/confirmacion.html', {'orden': orden})
