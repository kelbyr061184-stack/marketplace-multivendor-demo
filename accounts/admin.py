from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Usuario, Tienda

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'tipo_usuario', 'telefono', 'fecha_registro', 'is_active', 'is_staff')

class UsuarioAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = UsuarioResource
    list_display = ('username', 'email', 'tipo_usuario', 'telefono', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('tipo_usuario', 'telefono', 'fecha_registro')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('tipo_usuario', 'telefono')}),
    )

class TiendaResource(resources.ModelResource):
    class Meta:
        model = Tienda
        fields = ('id', 'vendedor__username', 'nombre_tienda', 'descripcion', 'ciudad', 'provincia', 'activa', 'fecha_creacion')

@admin.register(Tienda)
class TiendaAdmin(ImportExportModelAdmin):
    resource_class = TiendaResource
    list_display = ('nombre_tienda', 'vendedor', 'ciudad', 'activa')
    list_filter = ('activa', 'ciudad')
    search_fields = ('nombre_tienda', 'vendedor__username')

admin.site.register(Usuario, UsuarioAdmin)