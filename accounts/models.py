from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
        ('ambos', 'Comprador y Vendedor'),  # NUEVA OPCIÓN
    )
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default='comprador',
        help_text='Indica si el usuario es comprador, vendedor o ambos'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        help_text='Número de teléfono de contacto (opcional)'
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha y hora en que se registró el usuario'
    )

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Tienda(models.Model):
    vendedor = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tienda',
        limit_choices_to={'tipo_usuario__in': ['vendedor', 'ambos']},  # Ahora también acepta 'ambos'
        help_text='Usuario vendedor asociado a esta tienda'
    )
    nombre_tienda = models.CharField(
        max_length=100,
        help_text='Nombre comercial de la tienda'
    )
    descripcion = models.TextField(
        max_length=500,
        blank=True,
        help_text='Breve descripción de la tienda (opcional)'
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
        help_text='Dirección física (calle y número)'
    )
    ciudad = models.CharField(
        max_length=50,
        blank=True,
        help_text='Ciudad donde se ubica la tienda'
    )
    provincia = models.CharField(
        max_length=50,
        blank=True,
        help_text='Provincia o estado'
    )
    codigo_postal = models.CharField(
        max_length=10,
        blank=True,
        help_text='Código postal'
    )
    logo = models.ImageField(
        upload_to='logos_tienda/',
        blank=True,
        null=True,
        help_text='Logo de la tienda (opcional)'
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha de creación de la tienda'
    )
    activa = models.BooleanField(
        default=True,
        help_text='Indica si la tienda está activa (visible)'
    )

    def __str__(self):
        return self.nombre_tienda

    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'