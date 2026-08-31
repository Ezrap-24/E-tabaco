from django import forms

from django.conf import settings

from .envio import REGIONES_CHILE


def _metodo_pago_choices():
    """Webpay solo aparece si esta habilitado (WEBPAY_HABILITADO). Mientras
    Transbank no certifique el sitio queda en stand-by: ni se muestra en el
    checkout ni se puede elegir."""
    choices = []
    if getattr(settings, 'WEBPAY_HABILITADO', False):
        choices.append(('webpay', 'Webpay Plus'))
    choices.append(('mercadopago', 'Mercado Pago'))
    choices.append(('transferencia', 'Transferencia Bancaria / Deposito'))
    return choices


class CheckoutForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Nombre y apellido'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'ct-input', 'placeholder': 'tu@email.com'}),
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': '+56 9 1234 5678'}),
    )
    direccion = forms.CharField(
        label='Dirección',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Calle, número, depto'}),
    )
    ciudad = forms.CharField(
        label='Ciudad',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Santiago'}),
    )
    region = forms.ChoiceField(
        label='Región',
        choices=[('', 'Selecciona tu región')] + REGIONES_CHILE,
        widget=forms.Select(attrs={'class': 'ct-input'}),
    )
    codigo_postal = forms.CharField(
        label='Código postal',
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': '7500000'}),
    )
    tipo_documento = forms.ChoiceField(
        label='Boleta o Factura',
        choices=[('boleta', 'Boleta'), ('factura', 'Factura')],
        initial='boleta',
        widget=forms.Select(attrs={'class': 'ct-input'}),
    )
    razon_social = forms.CharField(
        label='Razón Social (para Factura)',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Razón social de la empresa'}),
    )
    giro = forms.CharField(
        label='Giro (para Factura)',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Giro comercial'}),
    )
    rut_facturacion = forms.CharField(
        label='RUT (para Factura)',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': '76.123.456-7'}),
    )
    notas = forms.CharField(
        label='Notas para el pedido (opcional)',
        required=False,
        widget=forms.Textarea(attrs={'class': 'ct-input', 'rows': 3,
                                     'placeholder': 'Instrucciones de entrega, referencias, etc.'}),
    )
    acepta_terminos = forms.BooleanField(
        required=True,
        label='Confirmo que soy mayor de 18 años y acepto los términos y condiciones.',
    )
    metodo_pago = forms.ChoiceField(
        label='Método de pago',
        choices=_metodo_pago_choices(),
        initial='webpay' if getattr(settings, 'WEBPAY_HABILITADO', False) else 'mercadopago',
        widget=forms.RadioSelect,
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('tipo_documento') == 'factura':
            for campo, etiqueta in (
                ('razon_social', 'la Razón Social'),
                ('giro', 'el Giro'),
                ('rut_facturacion', 'el RUT'),
            ):
                if not cleaned_data.get(campo):
                    self.add_error(campo, f'Debes indicar {etiqueta} para facturar.')
        return cleaned_data
