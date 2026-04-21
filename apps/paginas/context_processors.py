from django.conf import settings


def empresa_context(request):
    """Hace los datos de la empresa disponibles en todos los templates."""
    return {
        'empresa_telefono': settings.EMPRESA_TELEFONO,
        'empresa_telefono_wsp': settings.EMPRESA_TELEFONO_WSP,
        'empresa_email': settings.EMPRESA_EMAIL,
        'envio_gratis_desde': settings.ENVIO_GRATIS_DESDE,
    }
