# Marketplace Multivendor (Cars & Motorcycles) — Demo

✅ **Live demo:** https://kelby1984.pythonanywhere.com  
✅ **Admin:** https://kelby1984.pythonanywhere.com/admin/  

## What’s included
- Multi-vendor: each seller has a mini-store (inventory page).
- Sellers can publish used cars and motorcycles.
- Detailed technical specification sheet (core feature).
- Powerful filters (brand/model/year/mileage/price/location) + comparison tool.
- Leads (requests) + internal messaging.
- Admin approval & export.

## Tech stack
Django 6, Bootstrap 5, django-allauth, django-filter, django-import-export, Stripe (optional).

## Run locally (SQLite)
```bash
python -m venv .venv
# activate venv
pip install -r requirements.txt
python manage.py migrate --settings=config.settings_local
python manage.py runserver --settings=config.settings_local
# Marketplace MultiVendor (Coches y Motos)

Plataforma tipo *online showroom* multiproveedor para publicar anuncios de coches y motos usados.

## Características principales

- Arquitectura multiproveedor: cada vendedor tiene una **mini-tienda** con inventario.
- Publicación de **coches** y **motos** con ficha técnica detallada.
- Búsqueda y filtrado (marca, modelo, año, kilometraje, precio, ubicación) con paginación.
- Comparador de vehículos.
- Mensajería interna (chat tipo bandeja de entrada).
- Leads/solicitudes: los compradores pueden enviar solicitudes desde el detalle del vehículo.
- Admin:
  - Aprobar anuncios (campo `activo`).
  - Gestionar y exportar datos (Import/Export).
  - Ver leads.
  - Configuración básica de plataforma (comisión y tarifas).
- Stripe básico para “Destacar” anuncios:
  - Verificación inmediata por `session_id` en `success_url`.
  - Webhook opcional para producción (idempotente).

---

## Requisitos

- Python 3.12+
- (Producción recomendada) PostgreSQL

---

## Instalación rápida (local con SQLite)

> Este proyecto incluye `config/settings_local.py` para ejecutar en SQLite y *AUTO_APPROVE_LISTINGS=True*.

### Windows / PowerShell

```powershell
cd C:\marketplace\marketplace
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate --settings=config.settings_local
python manage.py createsuperuser --settings=config.settings_local

$env:DJANGO_SETTINGS_MODULE="config.settings_local"
python populate_india_completo.py

python manage.py runserver --settings=config.settings_local
```

Abrir:
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Panel vendedor: http://127.0.0.1:8000/vendor/dashboard/

---

## Configuración Stripe (opcional)

Variables de entorno:

- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET` (si usas webhook)

Webhook endpoint:

- `/stripe/webhook/`

---

## Producción (guía corta)

1) Define variables de entorno:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=tu-dominio.com`
- Configura DB PostgreSQL en `config/settings.py` o con un `settings_prod.py`.

2) Ejecuta:

```bash
python manage.py migrate
python manage.py collectstatic
```

3) Servidor recomendado:

- Gunicorn (WSGI) + Nginx
- Media (uploads): disco o bucket compatible S3

---

## Notas de seguridad

- No subas `.env` al repositorio.
- Mantén `DEBUG=0` en producción.
- Configura HTTPS (necesario para login social y para Stripe).
