"""Envío de correo vía la API HTTP de Resend.

Se dejó de usar el backend SMTP de Django porque Railway bloquea las
conexiones salientes por el puerto 587 — todo envío fallaba con un
TimeoutError silencioso (atrapado por el try/except de cada llamada).
La API HTTP de Resend usa el puerto 443, que sí está disponible.
"""
import logging

import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_correo(destinatarios, asunto, texto, html=None):
    """Envía un correo por la API de Resend.

    En desarrollo (DEBUG=True) o si falta RESEND_API_KEY, solo lo imprime
    en consola — igual que hacía antes el backend 'console' de Django.
    No relanza excepciones: quien llama decide qué loguear si falla.
    """
    if isinstance(destinatarios, str):
        destinatarios = [destinatarios]

    if settings.DEBUG or not settings.RESEND_API_KEY:
        print(f"[EMAIL DEV] Para: {destinatarios}\nAsunto: {asunto}\n\n{texto}\n")
        return True

    resend.api_key = settings.RESEND_API_KEY
    params = {
        'from': settings.DEFAULT_FROM_EMAIL,
        'to': destinatarios,
        'subject': asunto,
        'text': texto,
    }
    if html:
        params['html'] = html

    try:
        resend.Emails.send(params)
        return True
    except Exception:
        logger.exception('Error enviando correo via Resend: %s', asunto)
        return False
