from django.db import models
from django.utils import timezone
from accounts.models import Tienda
from django.contrib.auth import get_user_model

User = get_user_model()

# ================= NUEVOS MODELOS =================
class Marca(models.Model):
    nombre = models.CharField(max_length=50)  # Ya no es unique=True globalmente
    tipo = models.CharField(
        max_length=10,
        choices=[('coche', 'Coche'), ('moto', 'Moto')],
        default='coche'
    )

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        unique_together = ('nombre', 'tipo')  # Permite Honda (coche) y Honda (moto)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(
        max_length=10,
        choices=[('coche', 'Coche'), ('moto', 'Moto')],
        default='coche'
    )

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        unique_together = ('marca', 'nombre')  # Un modelo es único dentro de su marca

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


# ================= MODELOS EXISTENTES MODIFICADOS =================
class Coche(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='coches')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='coches', limit_choices_to={'tipo': 'coche'})
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='coches')
    anio = models.IntegerField()  # antes 'año', cambiado a 'anio' para evitar problemas
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    kilometraje = models.IntegerField(help_text='Kilómetros recorridos')
    ubicacion = models.CharField(max_length=100, help_text='Ciudad o zona')
    tipo_combustible = models.CharField(
        max_length=20,
        choices=[
            ('gasolina', 'Gasolina'),
            ('diesel', 'Diésel'),
            ('hibrido', 'Híbrido'),
            ('electrico', 'Eléctrico'),
        ]
    )
    transmision = models.CharField(
        max_length=20,
        choices=[
            ('manual', 'Manual'),
            ('automatica', 'Automática'),
            ('semiautomatica', 'Semiautomática'),
        ]
    )
    cilindrada = models.CharField(max_length=10, blank=True, help_text='Ej: 1.6L, 2.0L')
    potencia = models.IntegerField(help_text='Caballos de fuerza (CV)', blank=True, null=True)
    num_puertas = models.IntegerField()
    color = models.CharField(max_length=30)
    num_plazas = models.IntegerField()
    carroceria = models.CharField(
        max_length=30,
        choices=[
            ('sedan', 'Sedán'),
            ('hatchback', 'Hatchback'),
            ('suv', 'SUV'),
            ('familiar', 'Familiar'),
            ('coupe', 'Coupé'),
            ('convertible', 'Convertible'),
            ('monovolumen', 'Monovolumen'),
            ('pickup', 'Pickup'),
        ],
        blank=True
    )
    traccion = models.CharField(
        max_length=20,
        choices=[
            ('delantera', 'Delantera'),
            ('trasera', 'Trasera'),
            ('4x4', '4x4 / Integral'),
        ],
        blank=True
    )
    direccion_asistida = models.BooleanField(default=True)
    aire_acondicionado = models.BooleanField(default=True)
    abs = models.BooleanField(default=True)
    airbags = models.IntegerField(blank=True, null=True)
    garantia = models.CharField(max_length=50, blank=True, help_text='Ej: 6 meses, 1 año')
    descripcion = models.TextField(max_length=1000, blank=True)
    imagen = models.ImageField(upload_to='coches/', blank=True, null=True)
    activo = models.BooleanField(default=False, help_text='Aprobado por administrador')
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    destacado = models.BooleanField(default=False, help_text='Anuncio destacado (requiere pago)')

    class Meta:
        verbose_name = 'Coche'
        verbose_name_plural = 'Coches'
        indexes = [
            models.Index(fields=['activo', 'destacado', 'fecha_publicacion']),
            models.Index(fields=['precio']),
            models.Index(fields=['anio']),
            models.Index(fields=['kilometraje']),
            models.Index(fields=['ubicacion']),
            models.Index(fields=['marca', 'modelo']),
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo.nombre} ({self.anio})"


class Moto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='motos')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='motos', limit_choices_to={'tipo': 'moto'})
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='motos')
    anio = models.IntegerField()  # antes 'año'
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    kilometraje = models.IntegerField(help_text='Kilómetros recorridos')
    ubicacion = models.CharField(max_length=100)
    tipo_moto = models.CharField(
        max_length=30,
        choices=[
            ('scooter', 'Scooter'),
            ('naked', 'Naked'),
            ('deportiva', 'Deportiva'),
            ('cruiser', 'Cruiser'),
            ('touring', 'Touring'),
            ('enduro', 'Enduro'),
            ('motocross', 'Motocross'),
            ('cafe_racer', 'Café Racer'),
        ],
        blank=True
    )
    cilindrada = models.CharField(max_length=10, help_text='Ej: 125cc, 600cc')
    potencia = models.IntegerField(help_text='Caballos de fuerza (CV)', blank=True, null=True)
    tipo_motor = models.CharField(max_length=30, blank=True, help_text='Ej: 2T, 4T, monocilíndrico, bicilíndrico')
    refrigeracion = models.CharField(max_length=30, blank=True, help_text='Aire, líquida')
    arranque = models.CharField(
        max_length=20,
        choices=[('electrico', 'Eléctrico'), ('patada', 'Patada'), ('ambos', 'Ambos')],
        blank=True
    )
    cambio = models.CharField(
        max_length=20,
        choices=[('manual', 'Manual'), ('automatico', 'Automático')],
        blank=True
    )
    num_marchas = models.IntegerField(blank=True, null=True)
    freno_delantera = models.CharField(max_length=30, blank=True, help_text='Disco, tambor')
    freno_trasera = models.CharField(max_length=30, blank=True, help_text='Disco, tambor')
    abs = models.BooleanField(default=False)
    capacidad_tanque = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text='Litros')
    peso = models.IntegerField(blank=True, null=True, help_text='kg')
    color = models.CharField(max_length=30)
    garantia = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(max_length=1000, blank=True)
    imagen = models.ImageField(upload_to='motos/', blank=True, null=True)
    activo = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    destacado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'
        indexes = [
            models.Index(fields=['activo', 'destacado', 'fecha_publicacion']),
            models.Index(fields=['precio']),
            models.Index(fields=['anio']),
            models.Index(fields=['kilometraje']),
            models.Index(fields=['ubicacion']),
            models.Index(fields=['marca', 'modelo']),
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo.nombre} ({self.anio})"


class Mensaje(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    asunto = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asunto} - de {self.emisor} a {self.receptor}"


class Lead(models.Model):
    """Solicitud / lead generado por un comprador interesado en un vehículo."""

    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('en_contacto', 'En contacto'),
        ('cerrado', 'Cerrado'),
        ('descartado', 'Descartado'),
    ]

    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='leads')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads_recibidos')
    comprador = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='leads_enviados', null=True, blank=True)

    tipo_vehiculo = models.CharField(max_length=10, choices=[('coche', 'Coche'), ('moto', 'Moto')])
    vehiculo_id = models.PositiveIntegerField()

    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    mensaje = models.TextField(max_length=2000, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='nuevo')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        indexes = [
            models.Index(fields=['tienda', 'estado', 'creado_en']),
            models.Index(fields=['tipo_vehiculo', 'vehiculo_id']),
        ]

    def __str__(self):
        return f"Lead {self.id} ({self.get_tipo_vehiculo_display()}) - {self.nombre}"


class PlataformaConfig(models.Model):
    """Configuración simple (comisiones y tarifas)."""

    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tarifa_publicacion_cents = models.PositiveIntegerField(default=0, help_text="0 = gratis")
    tarifa_destacado_cents = models.PositiveIntegerField(default=1000, help_text="en centavos")
    moneda = models.CharField(max_length=10, default='eur')
    auto_aprobar_listados = models.BooleanField(default=False)

    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración de plataforma'
        verbose_name_plural = 'Configuración de plataforma'

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PaymentTransaction(models.Model):
    """Registro local de una transacción Stripe (tarifa de publicación o destacado)."""

    KINDS = [
        ('publicacion', 'Tarifa de publicación'),
        ('destacado', 'Destacado'),
    ]
    STATUS = [
        ('creada', 'Creada'),
        ('pagada', 'Pagada'),
        ('fallida', 'Fallida'),
        ('reembolsada', 'Reembolsada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagos')
    kind = models.CharField(max_length=20, choices=KINDS)

    tipo_vehiculo = models.CharField(max_length=10, choices=[('coche', 'Coche'), ('moto', 'Moto')])
    vehiculo_id = models.PositiveIntegerField()

    moneda = models.CharField(max_length=10, default='eur')
    monto_cents = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=STATUS, default='creada')
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    pagado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Transacción de pago'
        verbose_name_plural = 'Transacciones de pago'
        indexes = [
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['tipo_vehiculo', 'vehiculo_id']),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} - {self.usuario} - {self.get_status_display()}"


class StripeEvent(models.Model):
    """Deduplicación básica de eventos Stripe (idempotencia)."""

    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=255)
    recibido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento Stripe'
        verbose_name_plural = 'Eventos Stripe'

    def __str__(self):
        return f"{self.event_type} ({self.event_id})"