from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import PerfilUsuario


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'autocomplete': 'email'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'current-password'})
    )


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Tu apellido'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class DireccionForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('telefono', 'direccion', 'ciudad', 'region', 'codigo_postal')
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'region': 'Región',
            'codigo_postal': 'Código Postal',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número, dpto'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Santiago'}),
            'region': forms.TextInput(attrs={'placeholder': 'Región Metropolitana'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': '7500000'}),
        }


class DetallesCuentaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Sincronizar username con email
        user.username = user.email
        if commit:
            user.save()
        return user


class CambioPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'current-password'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )
