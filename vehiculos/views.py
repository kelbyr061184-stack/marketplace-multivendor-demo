from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import stripe
from .models import Coche, Lead, Mensaje, Modelo, Moto, PaymentTransaction, PlataformaConfig, StripeEvent
from .forms import CocheForm, LeadForm, MotoForm
from .filters import CocheFilter, MotoFilter
from accounts.models import Tienda
from django.contrib.auth import get_user_model

User = get_user_model()

if getattr(settings, 'STRIPE_SECRET_KEY', ''):
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _get_config_safe():
    try:
        return PlataformaConfig.get_solo()
    except Exception:
        # Durante migraciones o si la tabla aún no existe
        return None


def _auto_aprobar_listados():
    if hasattr(settings, 'AUTO_APPROVE_LISTINGS'):
        return bool(settings.AUTO_APPROVE_LISTINGS)
    cfg = _get_config_safe()
    return bool(cfg.auto_aprobar_listados) if cfg else False


def _tarifa_destacado():
    cfg = _get_config_safe()
    if cfg:
        return cfg.tarifa_destacado_cents, cfg.moneda
    return 1000, 'eur'


def _tarifa_publicacion():
    cfg = _get_config_safe()
    if cfg:
        return cfg.tarifa_publicacion_cents, cfg.moneda
    return 0, 'eur'


def _vehiculo_for_user(tipo: str, pk: int, user):
    """Obtiene un vehículo; si no está activo, solo lo puede ver el dueño o admin."""
    if tipo == 'coche':
        vehiculo = get_object_or_404(Coche, pk=pk)
    else:
        vehiculo = get_object_or_404(Moto, pk=pk)

    if vehiculo.activo:
        return vehiculo

    if user.is_authenticated and (user.is_superuser or vehiculo.tienda.vendedor_id == user.id):
        return vehiculo

    # Ocultar no aprobados al público
    raise Http404

# ------------------------------
# Vistas públicas
# ------------------------------

def lista_vehiculos(request):
    base_coches = (
        Coche.objects.filter(activo=True)
        .select_related('marca', 'modelo', 'tienda')
        .order_by('-destacado', '-fecha_publicacion')
    )
    base_motos = (
        Moto.objects.filter(activo=True)
        .select_related('marca', 'modelo', 'tienda')
        .order_by('-destacado', '-fecha_publicacion')
    )

    coche_filter = CocheFilter(request.GET, queryset=base_coches)
    moto_filter = MotoFilter(request.GET, queryset=base_motos)

    per_page = getattr(settings, 'LISTINGS_PER_PAGE', 10)
    coche_paginator = Paginator(coche_filter.qs, per_page)
    moto_paginator = Paginator(moto_filter.qs, per_page)

    coche_page = coche_paginator.get_page(request.GET.get('cpage', 1))
    moto_page = moto_paginator.get_page(request.GET.get('mpage', 1))

    params_c = request.GET.copy()
    params_c.pop('cpage', None)
    coche_query = params_c.urlencode()

    params_m = request.GET.copy()
    params_m.pop('mpage', None)
    moto_query = params_m.urlencode()

    return render(request, 'vehiculos/lista_vehiculos.html', {
        'coche_filter': coche_filter,
        'moto_filter': moto_filter,
        'coche_page': coche_page,
        'moto_page': moto_page,
        'coche_query': coche_query,
        'moto_query': moto_query,
    })

def detalle_coche(request, pk):
    coche = get_object_or_404(Coche, pk=pk)
    if not coche.activo and not (request.user.is_authenticated and (request.user.is_superuser or coche.tienda.vendedor_id == request.user.id)):
        return HttpResponse(status=404)

    lead_form = LeadForm(initial={
        'nombre': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
    })

    if request.method == 'POST':
        lead_form = LeadForm(request.POST)
        if lead_form.is_valid():
            vendedor = coche.tienda.vendedor
            lead = lead_form.save(commit=False)
            lead.tienda = coche.tienda
            lead.vendedor = vendedor
            lead.comprador = request.user if request.user.is_authenticated else None
            lead.tipo_vehiculo = 'coche'
            lead.vehiculo_id = coche.id
            lead.save()

            # Si el comprador está logueado, además creamos un mensaje interno al vendedor
            if request.user.is_authenticated and request.user.id != vendedor.id:
                Mensaje.objects.create(
                    emisor=request.user,
                    receptor=vendedor,
                    asunto=f"Interés en coche: {coche.marca.nombre} {coche.modelo.nombre} ({coche.anio})",
                    cuerpo=lead.mensaje or "Estoy interesado en este vehículo. ¿Podemos coordinar?",
                )
            messages.success(request, "Solicitud enviada al vendedor.")
            return redirect('detalle_coche', pk=pk)

    return render(request, 'vehiculos/detalle_coche.html', {'vehiculo': coche, 'lead_form': lead_form})

def detalle_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if not moto.activo and not (request.user.is_authenticated and (request.user.is_superuser or moto.tienda.vendedor_id == request.user.id)):
        return HttpResponse(status=404)

    lead_form = LeadForm(initial={
        'nombre': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
    })

    if request.method == 'POST':
        lead_form = LeadForm(request.POST)
        if lead_form.is_valid():
            vendedor = moto.tienda.vendedor
            lead = lead_form.save(commit=False)
            lead.tienda = moto.tienda
            lead.vendedor = vendedor
            lead.comprador = request.user if request.user.is_authenticated else None
            lead.tipo_vehiculo = 'moto'
            lead.vehiculo_id = moto.id
            lead.save()

            if request.user.is_authenticated and request.user.id != vendedor.id:
                Mensaje.objects.create(
                    emisor=request.user,
                    receptor=vendedor,
                    asunto=f"Interés en moto: {moto.marca.nombre} {moto.modelo.nombre} ({moto.anio})",
                    cuerpo=lead.mensaje or "Estoy interesado en este vehículo. ¿Podemos coordinar?",
                )
            messages.success(request, "Solicitud enviada al vendedor.")
            return redirect('detalle_moto', pk=pk)

    return render(request, 'vehiculos/detalle_moto.html', {'vehiculo': moto, 'lead_form': lead_form})

def comparar(request):
    coche_ids = request.GET.getlist('coche')
    moto_ids = request.GET.getlist('moto')
    vehiculos = []
    for id in coche_ids:
        try:
            vehiculos.append(Coche.objects.get(pk=id, activo=True))
        except Coche.DoesNotExist:
            pass
    for id in moto_ids:
        try:
            vehiculos.append(Moto.objects.get(pk=id, activo=True))
        except Moto.DoesNotExist:
            pass
    return render(request, 'vehiculos/comparar.html', {'vehiculos': vehiculos})


def api_modelos_por_marca(request):
    """Endpoint simple para dropdown dependiente Marca → Modelos."""
    marca_id = request.GET.get('marca_id')
    tipo = request.GET.get('tipo')
    if not marca_id:
        return JsonResponse({'results': []})
    qs = Modelo.objects.filter(marca_id=marca_id)
    if tipo in ['coche', 'moto']:
        qs = qs.filter(tipo=tipo)
    data = [{'id': m.id, 'nombre': m.nombre} for m in qs.order_by('nombre')]
    return JsonResponse({'results': data})

# ------------------------------
# Panel del vendedor (CRUD)
# ------------------------------

@login_required
def mis_anuncios(request):
    try:
        tienda = request.user.tienda
    except Tienda.DoesNotExist:
        messages.warning(request, "Necesitas crear una tienda antes de publicar anuncios.")
        return redirect('vendor_dashboard')
    coches = Coche.objects.filter(tienda=tienda).select_related('marca', 'modelo').order_by('-fecha_publicacion')
    motos = Moto.objects.filter(tienda=tienda).select_related('marca', 'modelo').order_by('-fecha_publicacion')
    return render(request, 'vehiculos/mis_anuncios.html', {
        'coches': coches,
        'motos': motos,
        'tienda': tienda,
    })

@login_required
def crear_coche(request):
    try:
        tienda = request.user.tienda
    except Tienda.DoesNotExist:
        messages.error(request, "Debes tener una tienda para publicar.")
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        form = CocheForm(request.POST, request.FILES)
        if form.is_valid():
            coche = form.save(commit=False)
            coche.tienda = tienda
            coche.activo = _auto_aprobar_listados()
            coche.save()
            if coche.activo:
                messages.success(request, "Coche publicado correctamente.")
            else:
                messages.info(request, "Coche enviado a revisión. Lo verás publicado cuando el administrador lo apruebe.")
            return redirect('mis_anuncios')
    else:
        form = CocheForm()
    return render(request, 'vehiculos/form_coche.html', {'form': form, 'accion': 'Publicar coche'})

@login_required
def crear_moto(request):
    try:
        tienda = request.user.tienda
    except Tienda.DoesNotExist:
        messages.error(request, "Debes tener una tienda para publicar.")
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        form = MotoForm(request.POST, request.FILES)
        if form.is_valid():
            moto = form.save(commit=False)
            moto.tienda = tienda
            moto.activo = _auto_aprobar_listados()
            moto.save()
            if moto.activo:
                messages.success(request, "Moto publicada correctamente.")
            else:
                messages.info(request, "Moto enviada a revisión. La verás publicada cuando el administrador la apruebe.")
            return redirect('mis_anuncios')
    else:
        form = MotoForm()
    return render(request, 'vehiculos/form_moto.html', {'form': form, 'accion': 'Publicar moto'})

@login_required
def editar_coche(request, pk):
    coche = get_object_or_404(Coche, pk=pk, tienda__vendedor=request.user)
    if request.method == 'POST':
        form = CocheForm(request.POST, request.FILES, instance=coche)
        if form.is_valid():
            obj = form.save(commit=False)
            # Si el admin no auto-aprueba, puede requerir re-revisión al editar
            if not _auto_aprobar_listados():
                obj.activo = False
            obj.save()
            messages.success(request, "Coche actualizado.")
            return redirect('mis_anuncios')
    else:
        form = CocheForm(instance=coche)
    return render(request, 'vehiculos/form_coche.html', {'form': form, 'accion': 'Editar coche'})

@login_required
def editar_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk, tienda__vendedor=request.user)
    if request.method == 'POST':
        form = MotoForm(request.POST, request.FILES, instance=moto)
        if form.is_valid():
            obj = form.save(commit=False)
            if not _auto_aprobar_listados():
                obj.activo = False
            obj.save()
            messages.success(request, "Moto actualizada.")
            return redirect('mis_anuncios')
    else:
        form = MotoForm(instance=moto)
    return render(request, 'vehiculos/form_moto.html', {'form': form, 'accion': 'Editar moto'})

@login_required
def eliminar_coche(request, pk):
    coche = get_object_or_404(Coche, pk=pk, tienda__vendedor=request.user)
    if request.method == 'POST':
        coche.delete()
        messages.success(request, "Coche eliminado.")
        return redirect('mis_anuncios')
    return render(request, 'vehiculos/confirmar_eliminar.html', {'vehiculo': coche, 'tipo': 'coche'})

@login_required
def eliminar_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk, tienda__vendedor=request.user)
    if request.method == 'POST':
        moto.delete()
        messages.success(request, "Moto eliminada.")
        return redirect('mis_anuncios')
    return render(request, 'vehiculos/confirmar_eliminar.html', {'vehiculo': moto, 'tipo': 'moto'})

# ------------------------------
# Pago con Stripe
# ------------------------------

@login_required
def pagar_destacar(request, tipo, pk):
    if tipo == 'coche':
        vehiculo = get_object_or_404(Coche, pk=pk, tienda__vendedor=request.user)
    elif tipo == 'moto':
        vehiculo = get_object_or_404(Moto, pk=pk, tienda__vendedor=request.user)
    else:
        messages.error(request, "Tipo de vehículo no válido.")
        return redirect('mis_anuncios')
    
    precio_destacar, moneda = _tarifa_destacado()
    if request.method == 'POST':
        try:
            if not getattr(settings, 'STRIPE_SECRET_KEY', ''):
                messages.error(request, "Stripe no está configurado en este entorno.")
                return redirect('mis_anuncios')

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': moneda,
                            'unit_amount': precio_destacar,
                            'product_data': {
                                'name': f'Destacar {vehiculo.marca} {vehiculo.modelo}',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('pago_exitoso', args=[tipo, pk])) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('mis_anuncios')),
                metadata={
                    'kind': 'destacado',
                    'tipo': tipo,
                    'vehiculo_id': str(pk),
                    'user_id': str(request.user.id),
                }
            )

            PaymentTransaction.objects.create(
                usuario=request.user,
                kind='destacado',
                tipo_vehiculo=tipo,
                vehiculo_id=pk,
                moneda=moneda,
                monto_cents=precio_destacar,
                stripe_session_id=checkout_session.id,
                status='creada',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            messages.error(request, f"Error al procesar el pago: {str(e)}")
            return redirect('mis_anuncios')
    return render(request, 'vehiculos/pagar_destacar.html', {'vehiculo': vehiculo, 'precio': precio_destacar/100})

@login_required
def pago_exitoso(request, tipo, pk):
    # Verificación inmediata por session_id (cuando Stripe está configurado)
    vehiculo = get_object_or_404(Coche if tipo == 'coche' else Moto, pk=pk, tienda__vendedor=request.user)
    session_id = request.GET.get('session_id')
    if getattr(settings, 'STRIPE_SECRET_KEY', '') and session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                vehiculo.destacado = True
                vehiculo.save(update_fields=['destacado'])

                PaymentTransaction.objects.filter(stripe_session_id=session_id).update(
                    status='pagada',
                    stripe_payment_intent_id=session.get('payment_intent', '') or '',
                    pagado_en=timezone.now(),
                )
                messages.success(request, "Pago verificado: tu anuncio ahora está destacado.")
            else:
                messages.warning(request, "No se pudo verificar el pago como 'paid'. Revisa tu panel.")
        except Exception:
            messages.warning(request, "No se pudo verificar el pago. Revisa tu panel.")
    else:
        # Modo demo (sin Stripe): no marcar automáticamente
        messages.info(request, "Stripe no está configurado. Configura STRIPE_SECRET_KEY para verificar pagos.")
    return redirect('mis_anuncios')


@csrf_exempt
def stripe_webhook(request):
    """Webhook Stripe: activa destacado/publicación solo cuando el pago está confirmado."""
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not endpoint_secret:
        return HttpResponse(status=400)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    # idempotencia
    if StripeEvent.objects.filter(event_id=event.id).exists():
        return HttpResponse(status=200)
    StripeEvent.objects.create(event_id=event.id, event_type=event.type)

    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id')
        metadata = session.get('metadata', {}) or {}
        kind = metadata.get('kind')
        tipo = metadata.get('tipo')
        vehiculo_id = metadata.get('vehiculo_id')

        if kind in ['destacado', 'publicacion'] and tipo in ['coche', 'moto'] and vehiculo_id:
            try:
                vehiculo_id_int = int(vehiculo_id)
                model = Coche if tipo == 'coche' else Moto
                vehiculo = model.objects.get(pk=vehiculo_id_int)

                if kind == 'destacado':
                    vehiculo.destacado = True
                    vehiculo.save(update_fields=['destacado'])
                elif kind == 'publicacion':
                    vehiculo.activo = True
                    vehiculo.save(update_fields=['activo'])

                PaymentTransaction.objects.filter(stripe_session_id=session_id).update(
                    status='pagada',
                    stripe_payment_intent_id=session.get('payment_intent', '') or '',
                    pagado_en=timezone.now(),
                )
            except Exception:
                pass

    return HttpResponse(status=200)

# ------------------------------
# Sistema de chat
# ------------------------------

@login_required
def bandeja_entrada(request):
    mensajes = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')
    return render(request, 'vehiculos/bandeja_entrada.html', {'mensajes': mensajes})

@login_required
def mensajes_enviados(request):
    mensajes = Mensaje.objects.filter(emisor=request.user).order_by('-fecha_envio')
    return render(request, 'vehiculos/mensajes_enviados.html', {'mensajes': mensajes})

@login_required
def enviar_mensaje(request, receptor_id=None):
    if receptor_id:
        receptor = get_object_or_404(User, pk=receptor_id)
    else:
        receptor = None
    if request.method == 'POST':
        receptor_id = request.POST.get('receptor_id')
        asunto = request.POST.get('asunto')
        cuerpo = request.POST.get('cuerpo')
        receptor = get_object_or_404(User, pk=receptor_id)
        Mensaje.objects.create(
            emisor=request.user,
            receptor=receptor,
            asunto=asunto,
            cuerpo=cuerpo
        )
        messages.success(request, "Mensaje enviado correctamente.")
        return redirect('bandeja_entrada')
    usuarios = User.objects.exclude(pk=request.user.pk)
    return render(request, 'vehiculos/enviar_mensaje.html', {'receptor': receptor, 'usuarios': usuarios})

@login_required
def ver_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)
    if mensaje.receptor != request.user and mensaje.emisor != request.user:
        messages.error(request, "No tienes permiso para ver este mensaje.")
        return redirect('bandeja_entrada')
    if mensaje.receptor == request.user and not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return render(request, 'vehiculos/ver_mensaje.html', {'mensaje': mensaje})


@login_required
def mis_leads(request):
    if request.user.tipo_usuario not in ['vendedor', 'ambos']:
        messages.error(request, "Solo vendedores pueden ver solicitudes.")
        return redirect('lista_vehiculos')

    tienda = getattr(request.user, 'tienda', None)
    if tienda is None:
        messages.warning(request, "No tienes tienda configurada.")
        return redirect('vendor_dashboard')

    estado = request.GET.get('estado')
    leads = Lead.objects.filter(tienda=tienda).select_related('comprador', 'vendedor').order_by('-creado_en')
    if estado in dict(Lead.ESTADOS):
        leads = leads.filter(estado=estado)

    return render(request, 'vehiculos/mis_leads.html', {'leads': leads, 'estado': estado, 'estados': Lead.ESTADOS})


@login_required
def ver_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if not (request.user.is_superuser or request.user.id in [lead.vendedor_id, lead.comprador_id]):
        messages.error(request, "No tienes permiso para ver esta solicitud.")
        return redirect('lista_vehiculos')

    if request.method == 'POST' and request.user.id == lead.vendedor_id:
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Lead.ESTADOS):
            lead.estado = nuevo_estado
            lead.save(update_fields=['estado', 'actualizado_en'])
            messages.success(request, "Estado actualizado.")
            return redirect('ver_lead', pk=pk)

    # Link al vehículo
    vehiculo_url = None
    if lead.tipo_vehiculo == 'coche':
        vehiculo_url = reverse('detalle_coche', args=[lead.vehiculo_id])
    else:
        vehiculo_url = reverse('detalle_moto', args=[lead.vehiculo_id])

    return render(request, 'vehiculos/ver_lead.html', {'lead': lead, 'vehiculo_url': vehiculo_url, 'estados': Lead.ESTADOS})