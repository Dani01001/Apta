import logging
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.utils.dateparse import parse_date
from django.utils import timezone
import json

from .models import Restaurante, Mesa, RestauranteAdmin
from Reservas.models import Reserva  # Asegúrese de que la ruta sea correcta

logger = logging.getLogger(__name__)


# === VISTAS PÚBLICAS ===

@require_GET
def lista_restaurantes(request):
    """Lista restaurantes activos con búsqueda y paginación."""
    query = request.GET.get('q', '').strip()
    restaurantes_list = Restaurante.objects.filter(activo=True).order_by('nombre')

    if query:
        restaurantes_list = restaurantes_list.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query)
        )

    paginator = Paginator(restaurantes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'restaurantes/lista.html', context)


@require_GET
def detalle_restaurante(request, slug):
    """Muestra detalles del restaurante según su slug."""
    restaurante = get_object_or_404(Restaurante, slug=slug, activo=True)

    plantilla_nombre = f"{restaurante.slug.replace('-', '_')}.html"
    plantilla_ruta = os.path.join('rest', plantilla_nombre)

    if not os.path.exists(os.path.join(settings.TEMPLATES[0]['DIRS'][0], plantilla_ruta)):
        return render(request, 'no_disponible.html', {'restaurante': restaurante})

    context = {'restaurante': restaurante}
    return render(request, plantilla_ruta, context)


# === PANEL ADMINISTRACIÓN RESTAURANTE ===

@login_required
def panel_admin_restaurante(request):
    """Panel principal para RestauranteAdmin."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        logger.warning(f"Acceso denegado al panel de admin. Usuario: {request.user.username}")
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante
    context = {'restaurante': restaurante, 'perfil_admin': perfil_admin}
    return render(request, 'restaurantes/panel_admin.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def gestionar_restaurante(request):
    """Panel de gestión del restaurante con reservas y mesas."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante

    if request.method == "POST" and request.POST.get("accion") == "editar_restaurante":
        restaurante.nombre = request.POST.get("nombre", restaurante.nombre)
        restaurante.descripcion = request.POST.get("descripcion", restaurante.descripcion)
        restaurante.direccion = request.POST.get("direccion", restaurante.direccion)
        restaurante.telefono = request.POST.get("telefono", restaurante.telefono)
        restaurante.email_contacto = request.POST.get("email_contacto", restaurante.email_contacto)
        restaurante.sitio_web = request.POST.get("sitio_web", restaurante.sitio_web)
        restaurante.horario_apertura = request.POST.get("horario_apertura", restaurante.horario_apertura)
        restaurante.horario_cierre = request.POST.get("horario_cierre", restaurante.horario_cierre)
        restaurante.save()
        return redirect('restaurantes:gestionar_restaurante')

    reservas = Reserva.objects.filter(mesa__restaurante=restaurante).select_related('mesa', 'usuario').order_by('-fecha', 'hora')
    hoy = timezone.localdate()
    reservas_hoy = reservas.filter(fecha=hoy).count()
    pendientes = reservas.filter(estado="Pendiente").count()
    confirmadas = reservas.filter(estado="Confirmada").count()
    canceladas = reservas.filter(estado="Cancelada").count()
    mesas = Mesa.objects.filter(restaurante=restaurante).order_by('numero')

    context = {
        'restaurante': restaurante,
        'perfil_admin': perfil_admin,
        'reservas': reservas,
        'mesas': mesas,
        'reservas_hoy': reservas_hoy,
        'pendientes': pendientes,
        'confirmadas': confirmadas,
        'canceladas': canceladas,
    }
    return render(request, 'gestionar_restaurante.html', context)


@csrf_exempt
@login_required
@require_POST
def actualizar_estado_reserva(request, reserva_id):
    """Actualiza el estado de una reserva vía AJAX."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return JsonResponse({'error': 'No tiene permisos para esta acción.'}, status=403)

    try:
        reserva = Reserva.objects.select_related('mesa__restaurante').get(id=reserva_id, mesa__restaurante=perfil_admin.restaurante)
    except Reserva.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada o no pertenece a su restaurante.'}, status=404)

    nuevo_estado = request.POST.get('estado')
    if nuevo_estado not in ['Pendiente', 'Confirmada', 'Cancelada']:
        return JsonResponse({'error': 'Estado inválido.'}, status=400)

    reserva.estado = nuevo_estado
    reserva.save()
    return JsonResponse({'success': True, 'nuevo_estado': nuevo_estado})
    
@csrf_exempt
def actualizar_estado_multiple(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                for reserva_id, nuevo_estado in data.items():
                    try:
                        reserva = Reserva.objects.get(id=reserva_id)
                        reserva.estado = nuevo_estado
                        reserva.save()
                    except Reserva.DoesNotExist:
                        continue
                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        return JsonResponse({"success": False, "error": "Método no permitido"})


# === MESAS ===

@login_required
@require_http_methods(["GET", "POST"])
def gestionar_mesas(request):
    """Lista y crea mesas del restaurante del admin."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante
    mesas = restaurante.mesas.all().order_by('numero')

    if request.method == 'POST':
        try:
            numero = int(request.POST.get('numero'))
            capacidad = int(request.POST.get('capacidad'))
            ubicacion = request.POST.get('ubicacion', '').strip()

            if Mesa.objects.filter(restaurante=restaurante, numero=numero).exists():
                context = {'restaurante': restaurante, 'mesas': mesas, 'error': f"Ya existe una mesa con el número {numero}."}
                return render(request, 'restaurantes/gestionar_mesas.html', context)

            Mesa.objects.create(restaurante=restaurante, numero=numero, capacidad=capacidad, ubicacion=ubicacion)
            return redirect('restaurantes:gestionar_mesas')

        except (ValueError, TypeError):
            context = {'restaurante': restaurante, 'mesas': mesas, 'error': "Datos de mesa inválidos."}
            return render(request, 'restaurantes/gestionar_mesas.html', context)
        except Exception as e:
            logger.error(f"Error al crear mesa: {e}")
            context = {'restaurante': restaurante, 'mesas': mesas, 'error': "Ocurrió un error al crear la mesa."}
            return render(request, 'restaurantes/gestionar_mesas.html', context)

    context = {'restaurante': restaurante, 'mesas': mesas}
    return render(request, 'restaurantes/gestionar_mesas.html', context)


@login_required
@require_POST
def eliminar_mesa(request, mesa_id):
    """Elimina una mesa específica del restaurante del admin."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No tienes permiso.'}, status=403)

    mesa = get_object_or_404(Mesa, id=mesa_id, restaurante=perfil_admin.restaurante)
    mesa.delete()
    return JsonResponse({'success': True})


# === RESERVAS ===

@login_required
@require_GET
def ver_reservas_restaurante(request):
    """Vista de reservas para el admin del restaurante."""
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante
    reservas = Reserva.objects.filter(restaurante=restaurante).order_by('-fecha', 'hora').select_related('mesa', 'usuario')
    paginator = Paginator(reservas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'restaurante': restaurante, 'page_obj': page_obj}
    return render(request, 'restaurantes/ver_reservas.html', context)


# === API MESAS DISPONIBLES ===

@csrf_exempt
@require_GET
def api_obtener_mesas_disponibles(request, restaurante_id):
    """API para obtener mesas disponibles para una fecha/hora específica."""
    try:
        restaurante = Restaurante.objects.get(id=restaurante_id, activo=True)
    except Restaurante.DoesNotExist:
        return JsonResponse({'error': 'Restaurante no encontrado o inactivo'}, status=404)

    fecha_str = request.GET.get('fecha')
    hora_str = request.GET.get('hora')
    if not fecha_str or not hora_str:
        return JsonResponse({'error': 'Se requieren los parámetros fecha y hora'}, status=400)

    try:
        fecha = parse_date(fecha_str)
        hora = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha u hora inválido'}, status=400)

    fecha_hora_inicio = datetime.combine(fecha, hora)
    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=1)
    mesas_disponibles = []

    for mesa in restaurante.mesas.all():
        reservas_solapadas = Reserva.objects.filter(mesa=mesa, fecha=fecha)
        if not any(fecha_hora_inicio < datetime.combine(r.fecha, r.hora) + timedelta(hours=getattr(r, 'duracion_horas', 1)) and
                   fecha_hora_fin > datetime.combine(r.fecha, r.hora) for r in reservas_solapadas):
            mesas_disponibles.append(mesa)

    mesas_data = [{'id': m.id, 'numero': m.numero, 'capacidad': m.capacidad, 'ubicacion': m.ubicacion} for m in mesas_disponibles]
    return JsonResponse({'mesas_disponibles': mesas_data})


# === AJAX: AGREGAR / EDITAR MESA ===

@login_required
@csrf_exempt
@require_POST
def agregar_mesa_ajax(request):
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No tiene permiso.'}, status=403)

    restaurante = perfil_admin.restaurante
    numero = request.POST.get('numero')
    capacidad = request.POST.get('capacidad')
    ubicacion = request.POST.get('ubicacion', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()

    if not numero or not capacidad:
        return JsonResponse({'success': False, 'error': 'Número y capacidad son requeridos.'}, status=400)

    if Mesa.objects.filter(restaurante=restaurante, numero=numero).exists():
        return JsonResponse({'success': False, 'error': f'Ya existe una mesa con el número {numero}.'}, status=400)

    try:
        Mesa.objects.create(restaurante=restaurante, numero=numero, capacidad=capacidad, ubicacion=ubicacion, descripcion=descripcion)
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error al crear mesa vía AJAX: {e}")
        return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)


@login_required
@csrf_exempt
@require_POST
def editar_mesa_ajax(request, mesa_id):
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No tiene permiso.'}, status=403)

    restaurante = perfil_admin.restaurante
    try:
        mesa = Mesa.objects.get(id=mesa_id, restaurante=restaurante)
    except Mesa.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mesa no encontrada.'}, status=404)

    mesa.numero = request.POST.get('numero', mesa.numero)
    mesa.capacidad = request.POST.get('capacidad', mesa.capacidad)
    mesa.ubicacion = request.POST.get('ubicacion', mesa.ubicacion)
    mesa.descripcion = request.POST.get('descripcion', mesa.descripcion)
    mesa.save()
    return JsonResponse({'success': True})


