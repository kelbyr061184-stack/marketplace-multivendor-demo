import django_filters
from .models import Marca, Modelo, Coche, Moto

class CocheFilter(django_filters.FilterSet):
    # Filtros numéricos
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte', label='Precio mínimo')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte', label='Precio máximo')
    anio_min = django_filters.NumberFilter(field_name='anio', lookup_expr='gte', label='Año mínimo')
    anio_max = django_filters.NumberFilter(field_name='anio', lookup_expr='lte', label='Año máximo')
    kilometraje_min = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='gte', label='Kilometraje mínimo')
    kilometraje_max = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='lte', label='Kilometraje máximo')

    # Filtros de opciones
    marca = django_filters.ModelChoiceFilter(queryset=Marca.objects.filter(tipo='coche'), label='Marca')
    modelo = django_filters.ModelChoiceFilter(queryset=Modelo.objects.filter(tipo='coche'), label='Modelo')
    tipo_combustible = django_filters.ChoiceFilter(choices=Coche._meta.get_field('tipo_combustible').choices, label='Combustible')
    transmision = django_filters.ChoiceFilter(choices=Coche._meta.get_field('transmision').choices, label='Transmisión')
    carroceria = django_filters.ChoiceFilter(choices=Coche._meta.get_field('carroceria').choices, label='Carrocería')
    traccion = django_filters.ChoiceFilter(choices=Coche._meta.get_field('traccion').choices, label='Tracción')

    class Meta:
        model = Coche
        fields = {
            'marca': ['exact'],
            'modelo': ['exact'],
            'anio': ['gte', 'lte'],
            'precio': ['gte', 'lte'],
            'tipo_combustible': ['exact'],
            'transmision': ['exact'],
            'kilometraje': ['gte', 'lte'],
            'ubicacion': ['icontains'],
            'carroceria': ['exact'],
            'traccion': ['exact'],
        }


class MotoFilter(django_filters.FilterSet):
    # Filtros numéricos
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte', label='Precio mínimo')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte', label='Precio máximo')
    anio_min = django_filters.NumberFilter(field_name='anio', lookup_expr='gte', label='Año mínimo')
    anio_max = django_filters.NumberFilter(field_name='anio', lookup_expr='lte', label='Año máximo')
    kilometraje_min = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='gte', label='Kilometraje mínimo')
    kilometraje_max = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='lte', label='Kilometraje máximo')
    # Nota: cilindrada es CharField (ej: "600cc"). Para rangos numéricos reales conviene normalizar.
    cilindrada = django_filters.CharFilter(field_name='cilindrada', lookup_expr='icontains', label='Cilindrada (texto)')

    # Filtros de opciones
    marca = django_filters.ModelChoiceFilter(queryset=Marca.objects.filter(tipo='moto'), label='Marca')
    modelo = django_filters.ModelChoiceFilter(queryset=Modelo.objects.filter(tipo='moto'), label='Modelo')
    tipo_moto = django_filters.ChoiceFilter(choices=Moto._meta.get_field('tipo_moto').choices, label='Tipo de moto')
    arranque = django_filters.ChoiceFilter(choices=Moto._meta.get_field('arranque').choices, label='Arranque')
    cambio = django_filters.ChoiceFilter(choices=Moto._meta.get_field('cambio').choices, label='Cambio')
    abs = django_filters.BooleanFilter(label='ABS')

    class Meta:
        model = Moto
        fields = {
            'marca': ['exact'],
            'modelo': ['exact'],
            'anio': ['gte', 'lte'],
            'precio': ['gte', 'lte'],
            'tipo_moto': ['exact'],
            'cilindrada': ['icontains'],
            'kilometraje': ['gte', 'lte'],
            'ubicacion': ['icontains'],
            'arranque': ['exact'],
            'cambio': ['exact'],
            'abs': ['exact'],
        }