"""Flujo de checkout y pago.

Diseño:
1. POST /pedidos/checkout/      → valida el formulario, crea una `Orden` en
   estado `pendiente_pago` con sus `DetallePedido`, crea el PaymentIntent de
   Stripe pasándole `metadata={'orden_id': str(orden.id)}`, y muestra la
   página de pago con el `client_secret`.
2. POST /pedidos/webhook/       → al recibir `payment_intent.succeeded`,
   busca la orden por el `orden_id` del metadata y la marca como `pagado`.
   Esta vista NO necesita acceso a la sesión del cliente, lo cual es lo
   correcto porque el webhook lo invoca Stripe.
3. GET  /pedidos/confirmacion/  → muestra al cliente la última orden creada
   (referenciada por sesión).
"""
from decimal import Decimal
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.carrito.carrito import Carrito
from .forms import CheckoutForm
from .models import DetallePedido, Orden

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def _datos_iniciales_checkout(request):
    """Pre-llena el form si el usuario está autenticado y tiene perfil con dirección."""
    if not request.user.is_authenticated:
        return {}
    user = request.user
    initial = {
        'nombre': user.get_full_name() or '',
        'email':  user.email,
    }
    perfil = getattr(user, 'perfil', None)
    if perfil:
        initial.update({
            'telefono':      perfil.telefono,
            'direccion':     perfil.direccion,
            'ciudad':        perfil.ciudad,
            'region':        perfil.region,
            'codigo_postal': perfil.codigo_postal,
        })
    return initial


def checkout(request):
    carrito = Carrito(request)
    if len(carrito) == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('carrito:ver')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            orden = _crear_orden_pendiente(request, form, carrito)
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(orden.total),  # CLP no tiene centavos
                    currency=settings.STRIPE_CURRENCY,
                    metadata={'orden_id': str(orden.id), 'numero_orden': orden.numero_orden},
                    receipt_email=orden.cliente_email,
                )
            except stripe.error.StripeError as e:
                logger.exception('Stripe falló al crear PaymentIntent')
                orden.estado = 'cancelado'
                orden.save(update_fields=['estado'])
                messages.error(request, 'No se pudo iniciar el pago. Intenta nuevamente más tarde.')
                return redirect('carrito:ver')

            orden.stripe_payment_intent = intent.id
            orden.save(update_fields=['stripe_payment_intent'])

            request.session['orden_pendiente_id'] = orden.id
            return render(request, 'pedidos/checkout_pago.html', {
                'orden': orden,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
            })
    else:
        form = CheckoutForm(initial=_datos_iniciales_checkout(request))

    return render(request, 'pedidos/checkout.html', {'form': form, 'carrito': carrito})


@transaction.atomic
def _crear_orden_pendiente(request, form, carrito):
    """Crea la Orden y sus DetallePedido en estado pendiente_pago."""
    cd = form.cleaned_data
    orden = Orden.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        cliente_nombre=cd['nombre'],
        cliente_email=cd['email'],
        cliente_telefono=cd.get('telefono', ''),
        direccion=cd['direccion'],
        ciudad=cd['ciudad'],
        region=cd['region'],
        codigo_postal=cd.get('codigo_postal', ''),
        notas=cd.get('notas', ''),
        total=carrito.total(),
        estado='pendiente_pago',
    )
    for item in carrito.items():
        DetallePedido.objects.create(
            orden=orden,
            producto=item['producto'],
            producto_nombre=item['producto'].nombre,
            tipo_venta=item['tipo_venta'],
            cantidad=item['cantidad'],
            precio_unitario=Decimal(str(item['precio'])),
        )
    return orden


@csrf_exempt
def stripe_webhook(request):
    """Stripe llama acá tras un evento de pago. Sin sesión de cliente disponible."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        logger.warning('Webhook Stripe con firma inválida')
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        _marcar_orden_pagada(event['data']['object'])
    elif event['type'] == 'payment_intent.payment_failed':
        _marcar_orden_fallida(event['data']['object'])

    return HttpResponse(status=200)


def _marcar_orden_pagada(payment_intent):
    orden_id = (payment_intent.get('metadata') or {}).get('orden_id')
    if not orden_id:
        logger.error('PaymentIntent sin orden_id en metadata: %s', payment_intent.get('id'))
        return
    try:
        orden = Orden.objects.get(id=orden_id)
    except Orden.DoesNotExist:
        logger.error('Orden %s no encontrada para PaymentIntent %s', orden_id, payment_intent.get('id'))
        return

    if orden.estado == 'pagado':
        return  # idempotente

    orden.estado = 'pagado'
    orden.fecha_pago = timezone.now()
    orden.save(update_fields=['estado', 'fecha_pago'])
    _enviar_email_confirmacion(orden)


def _marcar_orden_fallida(payment_intent):
    orden_id = (payment_intent.get('metadata') or {}).get('orden_id')
    if not orden_id:
        return
    Orden.objects.filter(id=orden_id, estado='pendiente_pago').update(estado='cancelado')


def _enviar_email_confirmacion(orden):
    asunto = f'Confirmación de pedido {orden.numero_orden} — Puro Tabaco'
    mensaje_html = render_to_string('email/confirmacion_pedido.html', {'orden': orden})
    send_mail(
        subject=asunto,
        message=f'Tu pedido {orden.numero_orden} fue confirmado. Total: ${orden.total}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[orden.cliente_email],
        html_message=mensaje_html,
        fail_silently=True,
    )


def confirmacion(request):
    """Página post-checkout: limpia el carrito y muestra la última orden."""
    orden_id = request.session.get('orden_pendiente_id')
    if not orden_id:
        return redirect('paginas:home')

    orden = get_object_or_404(Orden, id=orden_id)

    # Limpiamos el carrito y la sesión solo cuando el pago ya está confirmado.
    if orden.estado in ('pagado', 'preparando', 'enviado', 'entregado'):
        Carrito(request).limpiar()
        request.session.pop('orden_pendiente_id', None)

    return render(request, 'pedidos/confirmacion.html', {'orden': orden})
