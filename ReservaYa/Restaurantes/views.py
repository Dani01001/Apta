# ReservaYa/restaurantes/views.py
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from .models import Restaurante, Mesa, RestauranteAdmin
import os


from Reservas.models import Reserva  # Importa el modelo Reserva
from django.utils.dateparse import parse_date  # Importa parse_date


# Configurar logger (opcional pero útil para debugging)
logger = logging.getLogger(__name__)


@require_GET
def lista_restaurantes(request):
    """
    Vista pública para listar restaurantes.
    Permite búsqueda básica por nombre.
    """
    # Obtener parámetros de búsqueda
    query = request.GET.get('q', '').strip()
    
    # Filtrar restaurantes activos
    restaurantes_list = Restaurante.objects.filter(activo=True).order_by('nombre')
    
    # Aplicar búsqueda si hay término
    if query:
        restaurantes_list = restaurantes_list.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query)
        )
    
    # Paginación (por ejemplo, 10 por página)
    paginator = Paginator(restaurantes_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'restaurantes/lista.html', context)

# ... (dentro de views.py) ...

@require_GET
def detalle_restaurante(request, slug):
    """
    Vista pública para mostrar los detalles de un restaurante.
    Carga la plantilla específica en templates/rest/ según el slug del restaurante.
    """
    restaurante = get_object_or_404(Restaurante, slug=slug, activo=True)

    # Convertir guiones a guiones bajos para coincidir con nombres de archivo
    plantilla_nombre = f"{restaurante.slug.replace('-', '_')}.html"
    plantilla_ruta = os.path.join('rest', plantilla_nombre)

    # Verificar si la plantilla existe
    if not os.path.exists(os.path.join(settings.TEMPLATES[0]['DIRS'][0], plantilla_ruta)):
        # Si no existe, puede cargar una plantilla genérica o mostrar 404
        return render(request, 'restaurantes/no_disponible.html', {'restaurante': restaurante})

    context = {
        'restaurante': restaurante,
    }
    return render(request, plantilla_ruta, context)

# ... (dentro de views.py) ...

@login_required
def panel_admin_restaurante(request):
    """
    Vista principal del panel de administración para un RestauranteAdmin.
    Solo accesible por usuarios autenticados que sean RestauranteAdmin.
    """
    try:
        # Obtener el perfil de RestauranteAdmin del usuario logueado
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        # Si el usuario no es un RestauranteAdmin, denegar acceso
        logger.warning(f"Acceso denegado al panel de admin. Usuario: {request.user.username}")
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante

    # Aquí puedes agregar lógica para obtener datos para el dashboard
    # Por ejemplo, contar reservas recientes, ingresos, etc.
    # reservas_recientes = Reserva.objects.filter(restaurante=restaurante).order_by('-fecha')[:5]

    context = {
        'restaurante': restaurante,
        'perfil_admin': perfil_admin,
        # 'reservas_recientes': reservas_recientes,
    }
    return render(request, 'restaurantes/panel_admin.html', context)

# ... (importaciones adicionales al inicio si es necesario) ...
# from django import forms # Si usas formularios manuales
# from .forms import RestauranteForm # Si creas un formulario específico

@login_required
@require_http_methods(["GET", "POST"])
def gestionar_restaurante(request):
    """
    Vista para que un RestauranteAdmin pueda editar la información de su restaurante.
    """
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante

    if request.method == 'POST':
        # Procesar formulario de actualización
        # Aquí asumimos una actualización directa, pero lo ideal sería usar un Form o ModelForm
        restaurante.nombre = request.POST.get('nombre', restaurante.nombre)
        restaurante.descripcion = request.POST.get('descripcion', restaurante.descripcion)
        restaurante.direccion = request.POST.get('direccion', restaurante.direccion)
        restaurante.telefono = request.POST.get('telefono', restaurante.telefono)
        restaurante.email_contacto = request.POST.get('email_contacto', restaurante.email_contacto)
        restaurante.sitio_web = request.POST.get('sitio_web', restaurante.sitio_web)
        restaurante.horario_apertura = request.POST.get('horario_apertura', restaurante.horario_apertura)
        restaurante.horario_cierre = request.POST.get('horario_cierre', restaurante.horario_cierre)
        
        # Manejo de archivos (imágenes) - requiere manejo especial en el formulario HTML
        # if 'imagen_logo' in request.FILES:
        #     restaurante.imagen_logo = request.FILES['imagen_logo']
        # if 'imagen_portada' in request.FILES:
        #     restaurante.imagen_portada = request.FILES['imagen_portada']

        restaurante.save()
        # Redirigir o mostrar mensaje de éxito
        return redirect('panel_admin_restaurante') # Asegúrate de que este nombre de URL exista

    # Si es GET, mostrar el formulario con los datos actuales
    context = {
        'restaurante': restaurante,
    }
    return render(request, 'restaurantes/gestionar_restaurante.html', context)

# ... (dentro de views.py) ...

@login_required
@require_http_methods(["GET", "POST"])
def gestionar_mesas(request):
    """
    Vista combinada para listar y crear mesas del restaurante del admin.
    (Para editar/eliminar, se suelen usar vistas separadas o llamadas AJAX/API).
    """
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante
    mesas = restaurante.mesas.all().order_by('numero')

    if request.method == 'POST':
        # Lógica simple para crear una nueva mesa
        try:
            numero = int(request.POST.get('numero'))
            capacidad = int(request.POST.get('capacidad'))
            ubicacion = request.POST.get('ubicacion', '').strip()
            
                        # Verificar si ya existe una mesa con ese número
            if Mesa.objects.filter(restaurante=restaurante, numero=numero).exists():
                # Manejar error: mesa duplicada
                context = {
                    'restaurante': restaurante,
                    'mesas': mesas,
                    'error': f"Ya existe una mesa con el número {numero}."
                }
                # Volver a mostrar el formulario con el error
                return render(request, 'restaurantes/gestionar_mesas.html', context)
            else:  # <-- Este 'else' es clave
                # --- Si pasa todas las validaciones, crear la mesa ---
                Mesa.objects.create(
                    restaurante=restaurante,
                    numero=numero,
                    capacidad=capacidad,
                    ubicacion=ubicacion
                )
                # Redirigir para evitar reenvío del formulario y reflejar el cambio
                # Asegúrate de que 'gestionar_mesas' sea el nombre EXACTO de la URL
                return redirect('gestionar_mesas')
        except (ValueError, TypeError):
            # Manejar error: datos inválidos
            context = {
                'restaurante': restaurante,
                'mesas': mesas,
                'error': "Datos de mesa inválidos. Asegúrate de ingresar números válidos para número y capacidad."
            }
            return render(request, 'restaurantes/gestionar_mesas.html', context)
        except Exception as e:
            # Manejar otros errores
            logger.error(f"Error al crear mesa: {e}")
            context = {
                'restaurante': restaurante,
                'mesas': mesas,
                'error': "Ocurrió un error al crear la mesa."
            }
            return render(request, 'restaurantes/gestionar_mesas.html', context)

    # Si es GET, mostrar la lista
    context = {
        'restaurante': restaurante,
        'mesas': mesas,
    }
    return render(request, 'restaurantes/gestionar_mesas.html', context)

# Vistas separadas para editar y eliminar (ejemplo de eliminar)
@login_required
@require_POST
def eliminar_mesa(request, mesa_id):
    """
    Vista para eliminar una mesa específica del restaurante del admin.
    """
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No tienes permiso.'}, status=403)

    restaurante = perfil_admin.restaurante
    
    # Obtener la mesa y verificar que pertenece al restaurante del admin
    mesa = get_object_or_404(Mesa, id=mesa_id, restaurante=restaurante)
    
    # Opcional: Verificar si la mesa tiene reservas futuras antes de eliminar
    # from django.utils import timezone
    # if Reserva.objects.filter(mesa=mesa, fecha__gte=timezone.now().date()).exists():
    #     return JsonResponse({'success': False, 'error': 'No se puede eliminar una mesa con reservas futuras.'}, status=400)
    
    mesa.delete()
    return JsonResponse({'success': True})

# ... (importaciones necesarias) ...
# from reservas.models import Reserva # Ajusta la ruta según donde esté definido

@login_required
@require_GET
def ver_reservas_restaurante(request):
    """
    Vista para que un RestauranteAdmin vea las reservas de su restaurante.
    """
    try:
        perfil_admin = RestauranteAdmin.objects.select_related('restaurante').get(usuario=request.user)
    except RestauranteAdmin.DoesNotExist:
        return HttpResponseForbidden(render(request, 'restaurantes/no_tienes_permiso.html'))

    restaurante = perfil_admin.restaurante
    
    # Obtener reservas del restaurante, ordenadas por fecha y hora
    # Puedes agregar filtros por fecha aquí si es necesario
    reservas = Reserva.objects.filter(restaurante=restaurante).order_by('-fecha', 'hora').select_related('mesa', 'usuario')
    
    # Paginación opcional
    paginator = Paginator(reservas, 20) # 20 reservas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'restaurante': restaurante,
        'page_obj': page_obj,
    }
    return render(request, 'restaurantes/ver_reservas.html', context)

# ... (importaciones necesarias) ...
# import json
# from django.views.decorators.csrf import csrf_exempt # Solo si es una API pura sin CSRF
# from django.utils.dateparse import parse_date
# from datetime import datetime

@csrf_exempt # O usa DRF para manejar esto mejor
@require_http_methods(["GET"]) # O POST si envías datos complejos
def api_obtener_mesas_disponibles(request, restaurante_id):
    """
    Vista API para obtener mesas disponibles de un restaurante en una fecha/hora.
    Esta es una versión simplificada. La lógica de verificación de solapamiento
    debería ser más robusta (ver `crear_reserva` en `reservas/views.py`).
    """
    # Autenticación: Solo usuarios logueados?
    # if not request.user.is_authenticated:
    #     return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    try:
        restaurante = Restaurante.objects.get(id=restaurante_id, activo=True)
    except Restaurante.DoesNotExist:
        return JsonResponse({'error': 'Restaurante no encontrado o inactivo'}, status=404)

    # Obtener parámetros de la solicitud
    fecha_str = request.GET.get('fecha')
    hora_str = request.GET.get('hora')
    # duracion_horas_str = request.GET.get('duracion_horas', '1') # Opcional

    if not fecha_str or not hora_str:
        return JsonResponse({'error': 'Se requieren los parámetros fecha y hora'}, status=400)

    try:
        fecha = parse_date(fecha_str)
        hora = datetime.strptime(hora_str, '%H:%M').time()
        # duracion_horas = int(duracion_horas_str)
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha u hora inválido'}, status=400)

    # --- Lógica de disponibilidad (SIMPLIFICADA) ---
    # 1. Obtener todas las mesas del restaurante
    todas_las_mesas = list(restaurante.mesas.all())

    # 2. Obtener mesas ya reservadas para esa fecha/hora
    # Esta es una simplificación. La lógica real debe verificar solapamientos de horarios.
    # reservas_para_fecha = Reserva.objects.filter(restaurante=restaurante, fecha=fecha)
    # mesas_ocupadas_ids = reservas_para_fecha.values_list('mesa_id', flat=True)
    # mesas_disponibles = [m for m in todas_las_mesas if m.id not in mesas_ocupadas_ids]

    # --- Lógica de disponibilidad (CORRECTA, basada en `crear_reserva`) ---
    from datetime import datetime, timedelta
    fecha_hora_inicio = datetime.combine(fecha, hora)
    # Supongamos duración fija de 1 hora para este ejemplo
    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=1)

    mesas_disponibles = []
    for mesa in todas_las_mesas:
        # Verificar si hay reservas solapadas para esta mesa
        reservas_solapadas = Reserva.objects.filter(
            mesa=mesa,
            fecha=fecha,
        )
        solapada = False
        for r in reservas_solapadas:
            inicio_r = datetime.combine(r.fecha, r.hora)
            # Asumir duración de 1 hora si no está en el modelo o usar getattr
            duracion_r = getattr(r, 'duracion_horas', 1)
            fin_r = inicio_r + timedelta(hours=duracion_r)
            if (fecha_hora_inicio < fin_r and fecha_hora_fin > inicio_r):
                solapada = True
                break
        if not solapada:
            mesas_disponibles.append(mesa)

    # Serializar las mesas disponibles para JSON
    mesas_data = []
    for mesa in mesas_disponibles:
        mesas_data.append({
            'id': mesa.id,
            'numero': mesa.numero,
            'capacidad': mesa.capacidad,
            'ubicacion': mesa.ubicacion,
        })

    return JsonResponse({'mesas_disponibles': mesas_data})
