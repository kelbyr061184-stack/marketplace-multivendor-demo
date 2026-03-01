from django import forms

from .models import Coche, Lead, Modelo, Moto

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        exclude = ['tienda', 'activo', 'fecha_publicacion', 'destacado']  # Estos se asignan automáticamente
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limitar modelos por tipo y marca seleccionada
        self.fields['modelo'].queryset = Modelo.objects.filter(tipo='coche').order_by('marca__nombre', 'nombre')
        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = Modelo.objects.filter(tipo='coche', marca_id=marca_id).order_by('nombre')
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.marca_id:
            self.fields['modelo'].queryset = Modelo.objects.filter(tipo='coche', marca_id=self.instance.marca_id).order_by('nombre')

    def clean(self):
        cleaned = super().clean()
        marca = cleaned.get('marca')
        modelo = cleaned.get('modelo')
        if marca and modelo and modelo.marca_id != marca.id:
            self.add_error('modelo', 'El modelo no pertenece a la marca seleccionada.')
        return cleaned

class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        exclude = ['tienda', 'activo', 'fecha_publicacion', 'destacado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo'].queryset = Modelo.objects.filter(tipo='moto').order_by('marca__nombre', 'nombre')
        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = Modelo.objects.filter(tipo='moto', marca_id=marca_id).order_by('nombre')
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.marca_id:
            self.fields['modelo'].queryset = Modelo.objects.filter(tipo='moto', marca_id=self.instance.marca_id).order_by('nombre')

    def clean(self):
        cleaned = super().clean()
        marca = cleaned.get('marca')
        modelo = cleaned.get('modelo')
        if marca and modelo and modelo.marca_id != marca.id:
            self.add_error('modelo', 'El modelo no pertenece a la marca seleccionada.')
        return cleaned


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nombre', 'email', 'telefono', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu mensaje o solicitud de prueba de conducción...'}),
        }