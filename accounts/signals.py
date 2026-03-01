from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Tienda

@receiver(post_save, sender=Usuario)
def crear_tienda_para_vendedor(sender, instance, created, **kwargs):
    """Cuando se crea un usuario vendedor (o ambos), crear una tienda vacía."""
    if created and instance.tipo_usuario in ['vendedor', 'ambos']:
        Tienda.objects.create(
            vendedor=instance,
            nombre_tienda=f"Tienda de {instance.username}",
            descripcion="Descripción de la tienda (pendiente)",
            direccion="",
            ciudad="",
            provincia="",
            codigo_postal=""
        )