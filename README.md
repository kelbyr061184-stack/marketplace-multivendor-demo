# Marketplace Multivendor de Autos y Motos (Django) — Live Demo

🚗🏍️ Marketplace multiproveedor para **coches y motos usados**, con **mini-tiendas por vendedor**, publicación de anuncios, ficha técnica detallada, filtros avanzados, comparación y módulo de contacto (leads/mensajería).

✅ **Live demo:** https://kelby1984.pythonanywhere.com  
✅ **Repositorio:** https://github.com/kelbyr061184-stack/marketplace-multivendor-demo  
✅ **Release:** v1.0-demo

---

## Funcionalidades principales

### Para vendedores (mini-tiendas)
- Registro/login (multi-rol: comprador/vendedor).
- **Mini-tienda por vendedor** con inventario público.
- Publicación de anuncios de **coche** y **moto**.
- Panel del vendedor (gestión de anuncios y solicitudes/leads).

### Para compradores
- Navegación optimizada para “test drive”: listado claro, enfoque en datos y especificaciones.
- **Búsqueda y filtros**: marca, modelo, año, kilometraje, rango de precio, ubicación.
- **Comparador** de vehículos.
- **Ficha técnica completa** (core feature) en el detalle de cada anuncio.
- Contacto al vendedor vía **leads (solicitudes)** y mensajería interna.

### Administración
- Aprobación de listados (publicación moderada).
- Gestión de datos base (marcas/modelos).
- Exportación de datos (admin).
- Configuración básica de plataforma (tarifas/comisiones a nivel de config).

### Pagos (opcional)
- Integración base con **Stripe** para upgrades (por ejemplo, “destacar anuncio”).
- En demo pública los pagos pueden mantenerse desactivados (modo gratuito).

---

## Stack / Tecnologías
- **Backend:** Django 6
- **Frontend:** Bootstrap 5 (responsive)
- **Auth:** django-allauth (social login opcional en producción)
- **Filtros:** django-filter
- **Admin export:** django-import-export
- **Pagos (opcional):** Stripe

---

## Cómo probar (flujo recomendado)
1) Registrarse como **vendedor**
2) Crear la **mini-tienda**
3) Publicar 1 **coche** y 1 **moto**
4) Abrir el detalle de cada anuncio y revisar la **ficha técnica**
5) Probar filtros y comparación

> 💡 Para evaluación rápida, puedo facilitar credenciales demo por solicitud (no se publican en el repo por seguridad).

---

## Instalación local (SQLite)

### 1) Crear entorno e instalar dependencias
```bash
python -m venv .venv
# activar entorno
# Windows: .\.venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
