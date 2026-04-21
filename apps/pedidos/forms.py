from django import forms


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
    region = forms.CharField(
        label='Región',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': 'Región Metropolitana'}),
    )
    codigo_postal = forms.CharField(
        label='Código postal',
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ct-input', 'placeholder': '7500000'}),
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
