from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tienda
from .forms import TiendaForm
from vehiculos.models import Coche, Moto, Lead

@login_required
def vendor_dashboard(request):
    # Solo vendedores
    if request.user.tipo_usuario not in ['vendedor', 'ambos']:
        messages.error(request, "Tu cuenta no tiene perfil de vendedor. Cambia tu tipo de usuario o crea una cuenta de vendedor.")
        return redirect('lista_vehiculos')

    tienda = getattr(request.user, 'tienda', None)
    if tienda is None:
        messages.info(request, "Aún no tienes una tienda. Créala para publicar anuncios.")

    # Métricas rápidas
    coches = Coche.objects.filter(tienda=tienda) if tienda else Coche.objects.none()
    motos = Moto.objects.filter(tienda=tienda) if tienda else Moto.objects.none()
    leads_nuevos = Lead.objects.filter(tienda=tienda, estado='nuevo').count() if tienda else 0

    ctx = {
        'tienda': tienda,
        'total_coches': coches.count(),
        'total_motos': motos.count(),
        'pendientes_coches': coches.filter(activo=False).count(),
        'pendientes_motos': motos.filter(activo=False).count(),
        'leads_nuevos': leads_nuevos,
    }
    return render(request, 'vendor_dashboard.html', ctx)


@login_required
def tienda_crear_editar(request):
    """Crea o edita la tienda del vendedor (mini-tienda)."""
    if request.user.tipo_usuario not in ['vendedor', 'ambos']:
        messages.error(request, "Solo vendedores pueden crear/editar tiendas.")
        return redirect('lista_vehiculos')

    tienda = getattr(request.user, 'tienda', None)
    if request.method == 'POST':
        form = TiendaForm(request.POST, request.FILES, instance=tienda)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vendedor = request.user
            obj.save()
            messages.success(request, "Tienda guardada correctamente.")
            return redirect('vendor_dashboard')
    else:
        form = TiendaForm(instance=tienda)

    return render(request, 'tienda_form.html', {'form': form, 'tienda': tienda})


def tienda_publica(request, pk: int):
    """Página pública de la mini-tienda del vendedor."""
    tienda = get_object_or_404(Tienda, pk=pk, activa=True)
    coches = Coche.objects.filter(tienda=tienda, activo=True).select_related('marca', 'modelo').order_by('-destacado', '-fecha_publicacion')
    motos = Moto.objects.filter(tienda=tienda, activo=True).select_related('marca', 'modelo').order_by('-destacado', '-fecha_publicacion')
    return render(request, 'tienda_publica.html', {'tienda': tienda, 'coches': coches, 'motos': motos})