"""Integración con Webpay Plus (Transbank), como opción de pago junto a
Mercado Pago (ver `views.py`).

Flujo (Webpay Plus "normal", sin mall):
1. El checkout crea la `Orden` en `pendiente_pago` y llama a `crear_transaccion`.
   Transbank responde con una `url` y un `token`; el cliente debe hacer un POST
   con `token_ws=<token>` a esa `url` (la plantilla `webpay_redirigir.html`
   hace ese POST solo, con auto-submit).
2. Transbank redirige al cliente (con un POST) a `/pedidos/webpay/retorno/`
   con `token_ws` en el body. Ahí llamamos a `confirmar_transaccion` y, si
   `response_code == 0` y `status == 'AUTHORIZED'`, el pago fue aprobado.

Ambiente: por defecto usa el ambiente de integración/pruebas de Transbank
(`TBK_ENVIRONMENT=integration`), con el código de comercio y api key de
prueba públicos del SDK — no requiere configurar nada para probar con las
tarjetas de test de TransbankDevelopers. Para cobrar real hay que cambiar
`TBK_ENVIRONMENT=production` y cargar `TBK_COMMERCE_CODE`/`TBK_API_KEY`
reales (los que Transbank entrega al certificar la integración).
"""
from django.conf import settings
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction


def _transaction():
    """Arma el cliente `Transaction` según `TBK_ENVIRONMENT`."""
    if settings.TBK_ENVIRONMENT == 'production':
        options = WebpayOptions(
            settings.TBK_COMMERCE_CODE,
            settings.TBK_API_KEY,
            IntegrationType.LIVE,
        )
    else:
        # Ambiente de pruebas: si no se configuraron credenciales propias de
        # integración, usa las de prueba públicas que trae el SDK.
        options = WebpayOptions(
            settings.TBK_COMMERCE_CODE or IntegrationCommerceCodes.WEBPAY_PLUS,
            settings.TBK_API_KEY or IntegrationApiKeys.WEBPAY,
            IntegrationType.TEST,
        )
    return Transaction(options)


def crear_transaccion(orden, return_url):
    """Crea la transacción en Transbank. Devuelve (url, token) para el autosubmit."""
    monto = int(orden.total)  # CLP no usa decimales
    buy_order = orden.numero_orden[:26]  # Transbank exige <= 26 caracteres
    session_id = str(orden.id)[:61]
    respuesta = _transaction().create(buy_order, session_id, monto, return_url)
    return respuesta['url'], respuesta['token']


def confirmar_transaccion(token):
    """Hace el commit de la transacción. Devuelve el dict de respuesta de Transbank
    (incluye `response_code`, `status`, `authorization_code`, `amount`, etc.)."""
    return _transaction().commit(token)


def pago_aprobado(resultado):
    """True si el resultado del commit corresponde a un pago autorizado."""
    return resultado.get('response_code') == 0 and resultado.get('status') == 'AUTHORIZED'
