# Mercado multivendor de autos y motos usados (Django 6) — Live Demo

Aplicación web multiproveedor para publicar y explorar **autos y motos de segunda mano**.  
Cada vendedor puede crear su **mini-tienda**, publicar inventario y gestionar solicitudes de clientes.  
La prioridad del producto es la **ficha técnica detallada** por vehículo (core feature), con filtros avanzados y herramienta de comparación.

✅ **Demo en vivo:** https://kelby1984.pythonanywhere.com  
✅ **Release:** v1.0-demo  
✅ **Release link:** https://github.com/kelbyr061184-stack/marketplace-multivendor-demo/releases/tag/v1.0-demo  
✅ **Repositorio:** https://github.com/kelbyr061184-stack/marketplace-multivendor-demo

---

## 1) Qué puede probar un cliente en la demo (2–3 minutos)

1) Registrarse como **vendedor**  
2) Crear/editar su **mini-tienda**  
3) Publicar 1 **auto** y 1 **moto**  
4) Abrir el detalle del anuncio y revisar la **ficha técnica completa**  
5) Probar **búsqueda/filtros** y el **comparador**

> Para evaluación rápida se pueden facilitar credenciales demo por mensaje (no se publican en el repo por seguridad).

---

## 2) Alcance funcional (resumen)

### 2.1 Funcionalidades para vendedores (mini-tiendas)
- Registro/login con roles (comprador/vendedor).
- **Mini-tienda pública** por vendedor (perfil + inventario).
- Publicación de anuncios de **autos** y **motos**.
- Panel del vendedor: gestión de anuncios y **leads/solicitudes**.

### 2.2 Funcionalidades para compradores
- Listados de autos y motos con navegación centrada en datos.
- **Filtros avanzados:** marca, modelo, año, kilometraje, rango de precio, ubicación.
- **Comparador** de vehículos.
- Vista detalle con **tabla de especificaciones técnicas**.
- Contacto con el vendedor mediante **leads/solicitudes** y mensajería interna.

### 2.3 Administración
- Aprobación/moderación de listados (publicación controlada).
- Gestión de datos base (marcas/modelos).
- Exportación de datos desde admin.
- Configuración base de plataforma (tarifas/comisiones a nivel de configuración).

### 2.4 Pagos (opcional)
- Integración base con **Stripe** para upgrades (ej. “destacar anuncio”).
- En demo pública se puede mantener modo gratuito (sin pagos reales).

---

## 3) Qué NO incluye (para evitar malentendidos)
- Checkout de compra del vehículo (marketplaces de usados suelen funcionar por **leads**).
- Chat en tiempo real tipo WhatsApp (la demo incluye mensajería básica; realtime es un upgrade).
- Login social activo por defecto (requiere credenciales reales + HTTPS en producción).

---

## 4) Arquitectura / Módulos principales
- `accounts`: usuarios (roles), tiendas, panel del vendedor
- `vehiculos`: modelos de coche/moto, filtros, comparación, leads, mensajería, Stripe (opcional)
- `templates`: interfaz Bootstrap 5
- `config`: settings y urls del proyecto

---

## 5) Stack / Tecnologías
- **Backend:** Django 6
- **Frontend:** Bootstrap 5 (responsive)
- **Auth:** django-allauth (login social opcional en producción)
- **Filtros:** django-filter
- **Exportación admin:** django-import-export
- **Pagos (opcional):** Stripe

---

## 6) Instalación local (SQLite) — Paso a paso

### 6.1 Requisitos
- Python 3.12+ (Django 6 lo requiere)

### 6.2 Crear entorno e instalar dependencias
```bash
python -m venv .venv

# Activar entorno:
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
