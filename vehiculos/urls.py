from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('', views.lista_vehiculos, name='lista_vehiculos'),
    path('coche/<int:pk>/', views.detalle_coche, name='detalle_coche'),
    path('moto/<int:pk>/', views.detalle_moto, name='detalle_moto'),
    path('comparar/', views.comparar, name='comparar'),

    # API simple
    path('api/modelos/', views.api_modelos_por_marca, name='api_modelos_por_marca'),

    # Panel vendedor
    path('mis-anuncios/', views.mis_anuncios, name='mis_anuncios'),
    path('coche/nuevo/', views.crear_coche, name='crear_coche'),
    path('moto/nueva/', views.crear_moto, name='crear_moto'),
    path('coche/<int:pk>/editar/', views.editar_coche, name='editar_coche'),
    path('moto/<int:pk>/editar/', views.editar_moto, name='editar_moto'),
    path('coche/<int:pk>/eliminar/', views.eliminar_coche, name='eliminar_coche'),
    path('moto/<int:pk>/eliminar/', views.eliminar_moto, name='eliminar_moto'),

    # Pago
    path('pagar/<str:tipo>/<int:pk>/', views.pagar_destacar, name='pagar_destacar'),
    path('pago-exitoso/<str:tipo>/<int:pk>/', views.pago_exitoso, name='pago_exitoso'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),

    # Chat
    path('bandeja/', views.bandeja_entrada, name='bandeja_entrada'),
    path('enviados/', views.mensajes_enviados, name='mensajes_enviados'),
    path('enviar/<int:receptor_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensaje/<int:pk>/', views.ver_mensaje, name='ver_mensaje'),

    # Leads / solicitudes
    path('leads/', views.mis_leads, name='mis_leads'),
    path('lead/<int:pk>/', views.ver_lead, name='ver_lead'),
]