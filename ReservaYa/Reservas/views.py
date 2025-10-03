# ReservaYa/Reservas/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from .models import Reserva, Mesa
from .serializers import ReservaSerializer, CrearReservaSerializer
from Restaurantes.models import Restaurante  # Ajusta la ruta si es necesario
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from decimal import Decimal, InvalidOperation

# Vista para crear una reserva (API)
@csrf_exempt  # Desactivamos CSRF para esta vista API, pero en producción considera usar tokens
@require_http_methods(["POST"])
def crear_reserva_api(request):
    """
    Vista API para crear una nueva reserva.
    Recibe datos JSON en el cuerpo de la solicitud.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # Crear una instancia del serializador con los datos recibidos
    serializer = CrearReservaSerializer(data=data, context={'request': request})
    
    if serializer.is_valid():
        try:
            # El método `create` del serializador maneja la lógica de negocio
            reserva = serializer.save()
            # Serializar la reserva creada para la respuesta
            reserva_serializer = ReservaSerializer(reserva)
            return JsonResponse(reserva_serializer.data, status=201)
        except Exception as e:
            # Capturar errores específicos del serializador o de validación
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Si la validación falla, devolver errores del serializador
        return JsonResponse(serializer.errors, status=400)


# Vista para listar reservas del usuario autenticado (API)
@login_required
@require_http_methods(["GET"])
def mis_reservas_api(request):
    """
    Vista API para obtener las reservas del usuario autenticado.
    """
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', 'hora')
    serializer = ReservaSerializer(reservas, many=True)
    return JsonResponse(serializer.data, safe=False)


# Vista para cancelar una reserva (API)
@login_required
@require_http_methods(["DELETE"])  # O POST si prefieres un botón de "Cancelar"
def cancelar_reserva_api(request, reserva_id):
    """
    Vista API para cancelar una reserva específica del usuario.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    # Aquí podrías cambiar el estado en lugar de eliminar
    # reserva.estado = 'cancelada'
    # reserva.save()
    # O eliminarla físicamente
    reserva.delete()
    return JsonResponse({'message': 'Reserva cancelada'}, status=204) # 204 No Content


# Vista para editar una reserva (API)
@login_required
@require_http_methods(["PATCH"]) # O PUT si reemplazas todo el objeto
def editar_reserva_api(request, reserva_id):
    """
    Vista API para editar una reserva específica del usuario.
    Permite cambiar hora y cantidad de personas.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    nueva_hora_str = data.get('hora')
    nueva_cantidad_str = data.get('cantidad_personas')

    if not nueva_hora_str or not nueva_cantidad_str:
        return JsonResponse({'error': 'Hora y cantidad_personas son requeridos'}, status=400)

    # Validar y parsear la nueva hora
    try:
        nueva_hora = parse_time(nueva_hora_str)
        if not nueva_hora:
            raise ValueError("Formato de hora inválido")
    except ValueError:
        return JsonResponse({'error': 'Formato de hora inválido (HH:MM)'}, status=400)

    # Validar y parsear la nueva cantidad
    try:
        nueva_cantidad = int(nueva_cantidad_str)
        if nueva_cantidad <= 0:
             raise ValueError("La cantidad debe ser un número positivo")
    except ValueError:
        return JsonResponse({'error': 'cantidad_personas inválida'}, status=400)

    # Verificar capacidad de la mesa
    if nueva_cantidad > reserva.mesa.capacidad:
        return JsonResponse({'error': 'La nueva cantidad excede la capacidad de la mesa'}, status=400)

    # --- Verificar disponibilidad para la nueva hora ---
    # Calcular la nueva fecha/hora de inicio y fin
    nueva_fecha_hora_inicio = datetime.combine(reserva.fecha, nueva_hora)
    duracion_horas = float(getattr(reserva, 'duracion_horas', 1.0)) # Usar duración existente o 1h por defecto
    nueva_fecha_hora_fin = nueva_fecha_hora_inicio + timedelta(hours=duracion_horas)

    # Buscar reservas solapadas para la MISMA MESA (excluyendo la reserva actual)
    conflictos = Reserva.objects.filter(
        mesa=reserva.mesa,
        fecha=reserva.fecha,
    ).exclude(id=reserva.id) # Excluir la reserva que se está editando

    solapamiento = False
    for r_conflicto in conflictos:
        inicio_conflicto = datetime.combine(r_conflicto.fecha, r_conflicto.hora)
        duracion_conflicto = float(getattr(r_conflicto, 'duracion_horas', 1.0))
        fin_conflicto = inicio_conflicto + timedelta(hours=duracion_conflicto)

        # Verificar solapamiento: (nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente)
        if (nueva_fecha_hora_inicio < fin_conflicto and nueva_fecha_hora_fin > inicio_conflicto):
            solapamiento = True
            break

    if solapamiento:
        return JsonResponse({'error': 'La nueva hora solapa con otra reserva existente para esta mesa.'}, status=400)

    # --- Si pasa todas las validaciones, actualizar la reserva ---
    reserva.hora = nueva_hora
    reserva.cantidad_personas = nueva_cantidad
    reserva.save()

    # Serializar y devolver la reserva actualizada
    serializer = ReservaSerializer(reserva)
    return JsonResponse(serializer.data, status=200)


# Vista para obtener mesas disponibles (API auxiliar)
# Esta vista puede ser útil para el frontend para mostrar mesas disponibles
# antes de crear la reserva. La lógica es compleja, por lo que se simplifica aquí.
# En la práctica, esta lógica también puede residir en el serializador o en un servicio.
@csrf_exempt
@require_http_methods(["GET"])
def obtener_mesas_disponibles_api(request, restaurante_id):
    """
    Vista API auxiliar para obtener mesas disponibles para una fecha y hora específicas.
    Parámetros esperados en la URL: ?fecha=YYYY-MM-DD&hora=HH:MM&duracion=1.0&personas=N
    """
    try:
        restaurante = Restaurante.objects.get(id=restaurante_id, activo=True)
    except Restaurante.DoesNotExist:
        return JsonResponse({'error': 'Restaurante no encontrado o inactivo'}, status=404)

    fecha_str = request.GET.get('fecha')
    hora_str = request.GET.get('hora')
    duracion_str = request.GET.get('duracion', '1.0') # Valor por defecto
    personas_str = request.GET.get('personas')

    if not fecha_str or not hora_str or not personas_str:
        return JsonResponse({'error': 'Se requieren los parámetros: fecha, hora, personas'}, status=400)

    try:
        fecha = parse_date(fecha_str)
        hora = parse_time(hora_str)
        duracion_horas = float(duracion_str)
        cantidad_personas = int(personas_str)
        if cantidad_personas <= 0:
             raise ValueError()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Parámetros de fecha, hora, duracion o personas inválidos'}, status=400)

    # --- Lógica de disponibilidad (SIMPLIFICADA) ---
    # 1. Obtener todas las mesas del restaurante con suficiente capacidad
    mesas_posibles = Mesa.objects.filter(restaurante=restaurante, capacidad__gte=cantidad_personas)

    if not mesas_posibles.exists():
        return JsonResponse({'mesas_disponibles': []})

    # 2. Calcular el rango horario de la nueva reserva
    fecha_hora_inicio = datetime.combine(fecha, hora)
    fecha_hora_fin = fecha_hora_inicio + timedelta(hours=duracion_horas)

    mesas_disponibles = []
    for mesa in mesas_posibles:
        # Obtener reservas para esa mesa en esa fecha
        reservas_dia = Reserva.objects.filter(mesa=mesa, fecha=fecha)
        solapada = False
        for r in reservas_dia:
            inicio_r = datetime.combine(r.fecha, r.hora)
            duracion_r = float(getattr(r, 'duracion_horas', 1.0))
            fin_r = inicio_r + timedelta(hours=duracion_r)
            if (fecha_hora_inicio < fin_r and fecha_hora_fin > inicio_r):
                solapada = True
                break
        if not solapada:
            mesas_disponibles.append(mesa)

    # Serializar las mesas disponibles
    # Puedes crear un serializador específico para Mesa si es necesario
    mesas_data = []
    for mesa in mesas_disponibles:
        mesas_data.append({
            'id': mesa.id,
            'numero': mesa.numero,
            'capacidad': mesa.capacidad,
            'ubicacion': mesa.ubicacion
        })

    return JsonResponse({'mesas_disponibles': mesas_data})


# === VISTAS HTML (si decides tener algunas) ===

# Vista HTML para mostrar el formulario de reserva
# (Este sería un ejemplo muy básico, normalmente se maneja desde JS/frontend)
@login_required
def formulario_reserva_html(request):
    """
    Vista HTML para mostrar un formulario de reserva.
    (En la práctica, esto se haría principalmente con JS llamando a la API)
    """
    # Obtener restaurantes activos para el dropdown
    restaurantes = Restaurante.objects.filter(activo=True).order_by('nombre')
    context = {
        'restaurantes': restaurantes
    }
    return render(request, 'reservas/formulario_reserva.html', context)


# Vista HTML para mostrar las reservas del usuario
@login_required
def mis_reservas_html(request):
    """
    Vista HTML para mostrar las reservas del usuario autenticado.
    """
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', 'hora').select_related('mesa', 'mesa__restaurante')
    context = {
        'reservas': reservas
    }
    return render(request, 'reservas/mis_reservas.html', context)
