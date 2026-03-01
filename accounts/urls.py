from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('tienda/', views.tienda_crear_editar, name='tienda_crear_editar'),
    path('tienda/<int:pk>/', views.tienda_publica, name='tienda_publica'),
]