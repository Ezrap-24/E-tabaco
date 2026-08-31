from django.conf import settings


def empresa_context(request):
    """Hace los datos de la empresa disponibles en todos los templates."""
    return {
        'empresa_telefono': settings.EMPRESA_TELEFONO,
        'empresa_telefono_wsp': settings.EMPRESA_TELEFONO_WSP,
        'empresa_email': settings.EMPRESA_EMAIL,
        # Webpay en stand-by hasta que Transbank certifique el sitio.
        'webpay_habilitado': getattr(settings, 'WEBPAY_HABILITADO', False),
    }
