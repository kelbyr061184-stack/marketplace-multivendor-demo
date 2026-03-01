from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    Coche,
    Lead,
    Marca,
    Modelo,
    Mensaje,
    Moto,
    PaymentTransaction,
    PlataformaConfig,
    StripeEvent,
)

# ---------------------------
# Recursos para exportación
# ---------------------------
class CocheResource(resources.ModelResource):
    class Meta:
        model = Coche
        fields = ('id', 'tienda__vendedor__username', 'marca__nombre', 'modelo__nombre', 'anio', 'precio', 'kilometraje', 'ubicacion', 'activo', 'destacado')

class MotoResource(resources.ModelResource):
    class Meta:
        model = Moto
        fields = ('id', 'tienda__vendedor__username', 'marca__nombre', 'modelo__nombre', 'anio', 'precio', 'kilometraje', 'ubicacion', 'activo', 'destacado')

# ---------------------------
# Administración de Coches
# ---------------------------
@admin.register(Coche)
class CocheAdmin(ImportExportModelAdmin):
    resource_class = CocheResource
    list_display = ('marca', 'modelo', 'anio', 'precio', 'tienda', 'activo', 'destacado')
    list_filter = ('activo', 'destacado', 'marca', 'tipo_combustible', 'transmision')
    search_fields = ('marca__nombre', 'modelo__nombre', 'tienda__nombre_tienda')
    actions = ['activar_anuncios', 'destacar_anuncios']

    def activar_anuncios(self, request, queryset):
        queryset.update(activo=True)
    activar_anuncios.short_description = "Activar anuncios seleccionados"

    def destacar_anuncios(self, request, queryset):
        queryset.update(destacado=True)
    destacar_anuncios.short_description = "Destacar anuncios seleccionados"

# ---------------------------
# Administración de Motos
# ---------------------------
@admin.register(Moto)
class MotoAdmin(ImportExportModelAdmin):
    resource_class = MotoResource
    list_display = ('marca', 'modelo', 'anio', 'precio', 'tienda', 'activo', 'destacado')
    list_filter = ('activo', 'destacado', 'marca', 'tipo_moto')
    search_fields = ('marca__nombre', 'modelo__nombre', 'tienda__nombre_tienda')
    actions = ['activar_anuncios', 'destacar_anuncios']

    def activar_anuncios(self, request, queryset):
        queryset.update(activo=True)
    activar_anuncios.short_description = "Activar anuncios seleccionados"

    def destacar_anuncios(self, request, queryset):
        queryset.update(destacado=True)
    destacar_anuncios.short_description = "Destacar anuncios seleccionados"

# ---------------------------
# Administración de Mensajes
# ---------------------------
@admin.register(Mensaje)
class MensajeAdmin(ImportExportModelAdmin):
    list_display = ('asunto', 'emisor', 'receptor', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('asunto', 'emisor__username', 'receptor__username')

# ---------------------------
# Administración de Marcas
# ---------------------------
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

# ---------------------------
# Administración de Modelos
# ---------------------------
@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'tipo')
    list_filter = ('marca', 'tipo')
    search_fields = ('nombre', 'marca__nombre')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_vehiculo', 'vehiculo_id', 'tienda', 'nombre', 'email', 'telefono', 'estado', 'creado_en')
    list_filter = ('tipo_vehiculo', 'estado', 'creado_en')
    search_fields = ('nombre', 'email', 'telefono', 'tienda__nombre_tienda', 'vendedor__username')


@admin.register(PlataformaConfig)
class PlataformaConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'comision_porcentaje', 'tarifa_publicacion_cents', 'tarifa_destacado_cents', 'moneda', 'auto_aprobar_listados', 'actualizado_en')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'kind', 'tipo_vehiculo', 'vehiculo_id', 'monto_cents', 'moneda', 'status', 'creado_en', 'pagado_en')
    list_filter = ('kind', 'status', 'moneda')
    search_fields = ('usuario__username', 'stripe_session_id', 'stripe_payment_intent_id')


@admin.register(StripeEvent)
class StripeEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'event_id', 'recibido_en')
    search_fields = ('event_id', 'event_type')