"""Flujo de checkout y pago con Mercado Pago (Checkout Pro).

Diseno:
1. POST /pedidos/checkout/      -> valida el formulario, crea una `Orden` en
   estado `pendiente_pago` con sus `DetallePedido`, crea una *preferencia* de
   Mercado Pago con `external_reference=str(orden.id)` y redirige al cliente al
   `init_point` (la pagina segura de pago de Mercado Pago).
2. POST /pedidos/webhook/       -> Mercado Pago avisa aca cuando cambia el estado
   de un pago. Buscamos el pago por su id, leemos el `external_reference` para
   ubicar la orden y, si el pago esta `approved`, la marcamos como `pagado`.
   Esta vista NO necesita sesion del cliente: la invoca Mercado Pago.
3. GET  /pedidos/confirmacion/  -> el cliente vuelve aca tras pagar. Muestra la
   orden (por sesion o por `external_reference` que anade Mercado Pago a la URL).
"""
from decimal import Decimal
import json
import logging

import mercadopago
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.carrito.carrito import Carrito
from .emailing import enviar_correo
from .envio import calcular_envio, descripcion_envio
from .forms import CheckoutForm
from .models import ContadorOrden, DetallePedido, Orden

logger = logging.getLogger(__name__)


def _sdk():
    return mercadopago.SDK(settings.MP_ACCESS_TOKEN)


def _datos_iniciales_checkout(request):
    """Pre-llena el form si el usuario esta autenticado y tiene perfil con direccion."""
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
        messages.warning(request, 'Tu carrito esta vacio.')
        return redirect('carrito:ver')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            orden = _crear_orden_pendiente(request, form, carrito)
            try:
                preferencia = _crear_preferencia_mp(request, orden, carrito)
            except Exception:
                logger.exception('Mercado Pago fallo al crear la preferencia')
                orden.estado = 'cancelado'
                orden.save(update_fields=['estado'])
                messages.error(request, 'No se pudo iniciar el pago. Intenta nuevamente mas tarde.')
                return redirect('carrito:ver')

            # Guardamos el preference_id ANTES de redirigir, asi el webhook
            # siempre puede correlacionar el pago con la orden.
            with transaction.atomic():
                orden.mp_preference_id = preferencia['id']
                orden.save(update_fields=['mp_preference_id'])

            request.session['orden_pendiente_id'] = orden.id
            # Redirige a la pagina de pago segura de Mercado Pago.
            return redirect(preferencia['init_point'])
    else:
        form = CheckoutForm(initial=_datos_iniciales_checkout(request))

    return render(request, 'pedidos/checkout.html', {'form': form, 'carrito': carrito})


def _crear_preferencia_mp(request, orden, carrito):
    """Crea una preferencia de Checkout Pro y devuelve el dict de respuesta de MP."""
    items = [
        {
            'title': (item['nombre'] or item['producto'].nombre)[:250],
            'quantity': int(item['cantidad']),
            'unit_price': float(item['precio']),
            'currency_id': settings.MP_CURRENCY,
        }
        for item in carrito.items()
    ]
    if orden.costo_envio and orden.costo_envio > 0:
        items.append({
            'title': 'Despacho Región Metropolitana',
            'quantity': 1,
            'unit_price': float(orden.costo_envio),
            'currency_id': settings.MP_CURRENCY,
        })

    confirmacion_url = settings.SITE_URL + reverse('pedidos:confirmacion')
    preference_data = {
        'items': items,
        'external_reference': str(orden.id),
        'payer': {
            'name': orden.cliente_nombre,
            'email': orden.cliente_email,
        },
        'back_urls': {
            'success': confirmacion_url,
            'pending': confirmacion_url,
            'failure': settings.SITE_URL + reverse('pedidos:checkout'),
        },
        'statement_descriptor': 'PURO TABACO',
        'metadata': {'orden_id': str(orden.id), 'numero_orden': orden.numero_orden},
    }

    # auto_return y notification_url exigen URLs publicas (https). En local sin
    # tunel (localhost) se omiten para que la preferencia se cree igual; el
    # webhook se puede configurar tambien desde el panel de Mercado Pago.
    es_publica = settings.SITE_URL.startswith('https://')
    if es_publica:
        preference_data['auto_return'] = 'approved'
        preference_data['notification_url'] = settings.SITE_URL + reverse('pedidos:mp_webhook')

    resultado = _sdk().preference().create(preference_data)
    if resultado.get('status') not in (200, 201):
        logger.error('Respuesta inesperada de MP al crear preferencia: %s', resultado)
        raise RuntimeError('Mercado Pago no creo la preferencia')
    return resultado['response']


@transaction.atomic
def _crear_orden_pendiente(request, form, carrito):
    """Crea la Orden y sus DetallePedido en estado pendiente_pago."""
    cd = form.cleaned_data
    envio = calcular_envio(cd['region'])
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
        costo_envio=envio,
        total=carrito.total() + envio,
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
def mp_webhook(request):
    """Mercado Pago llama aca cuando cambia el estado de un pago.

    Acepta el formato nuevo (Webhooks: ?type=payment&data.id=...) y el legacy
    (IPN: ?topic=payment&id=...). Respondemos 200 siempre que el aviso sea
    valido para que Mercado Pago no siga reintentando.
    """
    tipo = request.GET.get('type') or request.GET.get('topic')
    payment_id = request.GET.get('data.id') or request.GET.get('id')

    # Algunos avisos traen los datos en el cuerpo JSON en vez de la query.
    if not payment_id and request.body:
        try:
            cuerpo = json.loads(request.body)
            tipo = tipo or cuerpo.get('type')
            payment_id = payment_id or (cuerpo.get('data') or {}).get('id')
        except (ValueError, AttributeError):
            pass

    if tipo and tipo != 'payment':
        return HttpResponse(status=200)  # ignoramos merchant_order, etc.
    if not payment_id:
        return HttpResponse(status=200)

    try:
        resultado = _sdk().payment().get(payment_id)
    except Exception:
        logger.exception('Error consultando el pago %s en Mercado Pago', payment_id)
        return HttpResponse(status=200)

    pago = resultado.get('response') or {}
    estado_pago = pago.get('status')
    orden_id = pago.get('external_reference')

    if estado_pago == 'approved':
        _marcar_orden_pagada(orden_id, str(payment_id))
    elif estado_pago in ('rejected', 'cancelled'):
        _marcar_orden_fallida(orden_id)

    return HttpResponse(status=200)


def _marcar_orden_pagada(orden_id, mp_payment_id=''):
    if not orden_id:
        logger.error('Pago aprobado sin external_reference (orden_id)')
        return
    try:
        orden = Orden.objects.get(id=orden_id)
    except (Orden.DoesNotExist, ValueError):
        logger.error('Orden %s no encontrada para el pago %s', orden_id, mp_payment_id)
        return

    if orden.estado == 'pagado':
        return  # idempotente

    orden.estado = 'pagado'
    orden.fecha_pago = timezone.now()
    orden.mp_payment_id = mp_payment_id
    if not orden.correlativo:
        orden.correlativo = ContadorOrden.siguiente()
    orden.save(update_fields=['estado', 'fecha_pago', 'mp_payment_id', 'correlativo'])
    _enviar_email_confirmacion(orden)
    _notificar_venta_admin(orden)


def _marcar_orden_fallida(orden_id):
    if not orden_id:
        return
    Orden.objects.filter(id=orden_id, estado='pendiente_pago').update(estado='cancelado')


def _enviar_email_confirmacion(orden):
    asunto = 'Confirmacion de pedido {} - Puro Tabaco'.format(orden.numero_orden)
    mensaje_html = render_to_string('email/confirmacion_pedido.html', {'orden': orden})
    try:
        enviar_correo(
            destinatarios=[orden.cliente_email],
            asunto=asunto,
            texto='Tu pedido {} fue confirmado. Total: ${}.'.format(orden.numero_orden, orden.total),
            html=mensaje_html,
        )
    except Exception:
        logger.exception('Error enviando email de confirmacion para orden %s', orden.numero_orden)


def _notificar_venta_admin(orden):
    """Avisa al correo del negocio cuando se concreta una venta."""
    destino = getattr(settings, 'VENTAS_NOTIFY_EMAIL', '') or settings.CONTACT_EMAIL
    if not destino:
        return
    lineas = [
        'Nueva venta confirmada: {}'.format(orden.folio),
        'Cliente: {} <{}>'.format(orden.cliente_nombre, orden.cliente_email),
        'Telefono: {}'.format(orden.cliente_telefono or '-'),
        'Direccion: {}'.format(orden.direccion_envio),
        'Subtotal productos: ${}'.format(orden.subtotal_productos),
        'Despacho: ${} ({})'.format(orden.costo_envio, descripcion_envio(orden.region)),
        'Total: ${}'.format(orden.total),
        '',
        'Detalle:',
    ]
    for d in orden.detalles.all():
        lineas.append('  - {}x {} ({}) = ${}'.format(
            d.cantidad, d.producto_nombre or d.producto.nombre, d.tipo_venta, d.subtotal()))
    try:
        enviar_correo(
            destinatarios=[destino],
            asunto='Nueva venta {} - ${} - Puro Tabaco'.format(orden.folio, orden.total),
            texto='\n'.join(lineas),
        )
    except Exception:
        logger.exception('Error enviando aviso de venta al negocio para orden %s', orden.numero_orden)


def confirmacion(request):
    """Pagina post-checkout: muestra la orden y limpia el carrito si ya esta paga.

    Mercado Pago devuelve al cliente con ?external_reference=<orden_id> en la URL,
    que usamos como respaldo si la sesion se perdio.
    """
    orden_id = request.session.get('orden_pendiente_id') or request.GET.get('external_reference')
    if not orden_id:
        return redirect('paginas:home')

    orden = get_object_or_404(Orden, id=orden_id)

    # Si el cliente volvio como aprobado pero el webhook aun no llega (comun en
    # local sin tunel), confirmamos consultando el pago directamente a MP.
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    if orden.estado == 'pendiente_pago' and payment_id:
        _confirmar_por_retorno(orden, payment_id)
        orden.refresh_from_db()

    # Limpiamos el carrito y la sesion solo cuando el pago ya esta confirmado.
    if orden.estado in ('pagado', 'preparando', 'enviado', 'entregado'):
        Carrito(request).limpiar()
        request.session.pop('orden_pendiente_id', None)

    return render(request, 'pedidos/confirmacion.html', {'orden': orden})


def _confirmar_por_retorno(orden, payment_id):
    """Verifica un pago contra la API de MP al volver el cliente (respaldo del webhook)."""
    try:
        resultado = _sdk().payment().get(payment_id)
    except Exception:
        logger.exception('Error verificando el pago %s al volver del checkout', payment_id)
        return
    pago = resultado.get('response') or {}
    if pago.get('status') == 'approved' and str(pago.get('external_reference')) == str(orden.id):
        _marcar_orden_pagada(str(orden.id), str(payment_id))


def comprobante_pdf(request, numero_orden):
    """Descarga el comprobante PDF de una orden. Solo accesible por el dueno o staff."""
    from django.http import HttpResponse, Http404
    from .comprobante import generar_comprobante

    orden = get_object_or_404(Orden, numero_orden=numero_orden)

    # Seguridad: solo el dueno de la orden o staff puede descargar
    if not request.user.is_staff:
        es_dueno = False
        if request.user.is_authenticated:
            # Usuario logueado: verificar por FK o por email
            es_dueno = (orden.usuario == request.user) or (orden.cliente_email == request.user.email)
        if not es_dueno:
            # Compra como invitado: verificar por sesion
            if request.session.get('orden_pendiente_id') != orden.id:
                raise Http404

    if orden.estado not in ('pagado', 'preparando', 'enviado', 'entregado'):
        raise Http404

    pdf_buf = generar_comprobante(orden)
    nombre_archivo = 'comprobante-{}.pdf'.format(orden.folio)

    response = HttpResponse(pdf_buf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(nombre_archivo)
    return response
