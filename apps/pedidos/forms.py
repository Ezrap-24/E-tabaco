from django import forms


class CheckoutForm(forms.Form):
    # Datos de envío
    nombre = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'})
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Dirección completa de envío'
        })
    )
    acepta_terminos = forms.BooleanField(
        required=True,
        label='Confirmo que soy mayor de 18 años y acepto los términos y condiciones.'
    )
