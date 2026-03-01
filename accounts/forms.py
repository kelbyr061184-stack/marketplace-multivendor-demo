from django import forms
from allauth.account.forms import SignupForm

from .models import Tienda, Usuario

class CustomSignupForm(SignupForm):
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_USUARIO_CHOICES,  # Ya incluye 'ambos'
        initial='comprador',
        label="Tipo de usuario"
    )

    def save(self, request):
        user = super().save(request)
        user.tipo_usuario = self.cleaned_data['tipo_usuario']
        user.save()
        return user


class TiendaForm(forms.ModelForm):
    """Formulario para crear/editar la mini-tienda del vendedor."""

    class Meta:
        model = Tienda
        fields = [
            'nombre_tienda',
            'descripcion',
            'direccion',
            'ciudad',
            'provincia',
            'codigo_postal',
            'logo',
            'activa',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }