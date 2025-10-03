# ReservaYa/Reservas/serializers.py
from rest_framework import serializers
# Importamos el modelo que acabamos de definir
from .models import Reserva
# También necesitamos serializadores para los modelos relacionados
# Si están en otras apps, los importamos. Asumo que Usuario está en 'Usuarios'
# y Mesa/Restaurante están en 'Restaurantes'. Ajusta las rutas según tu estructura real.
from Usuarios.models import Usuario # Ajusta si es necesario
from Restaurantes.models import Mesa, Restaurante # Ajusta si es necesario

# --- Serializadores para Modelos Relacionados (Opcionales pero útiles) ---

class UsuarioReservaSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para el usuario asociado a una reserva.
    Solo incluye campos esenciales.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email']
        read_only_fields = fields # Estos campos no se deberían modificar desde la Reserva

class MesaReservaSerializer(serializers.ModelSerializer):
    """
    Serializador para la mesa asociada a una reserva.
    """
    restaurante_nombre = serializers.CharField(source='restaurante.nombre', read_only=True)
    
    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'capacidad', 'restaurante_nombre']
        read_only_fields = fields

# --- Serializador Principal para el Modelo Reserva ---

class ReservaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Reserva.
    Incluye representaciones anidadas de Usuario y Mesa.
    """
    # Campos relacionales como objetos anidados (solo lectura por defecto)
    usuario = UsuarioReservaSerializer(read_only=True)
    mesa = MesaReservaSerializer(read_only=True)
    
    # Campos calculados o de conveniencia para el frontend
    restaurante_info = serializers.SerializerMethodField()
    mesa_numero = serializers.SerializerMethodField()
    codigo_reserva = serializers.CharField(read_only=True) # Es generado automáticamente

    class Meta:
        model = Reserva
        # Especificamos explícitamente los campos a incluir
        fields = [
            'id', 'codigo_reserva', 'nombre_cliente', 'fecha', 'hora', 'duracion_horas',
            'cantidad_personas', 'estado', 'fecha_creacion', 'fecha_actualizacion',
            'usuario', 'mesa', 'mesa_numero', 'restaurante_info'
        ]
        # Campos que no se pueden modificar directamente vía API
        read_only_fields = [
            'id', 'codigo_reserva', 'fecha_creacion', 'fecha_actualizacion',
            'usuario', 'mesa' # Estos se asignan por lógica, no por entrada directa
        ]
        
        # Validadores adicionales a nivel de campo (opcional)
        extra_kwargs = {
             'cantidad_personas': {'min_value': 1},
             'duracion_horas': {'min_value': 0.5, 'max_value': 24},
         }

    def get_restaurante_info(self, obj):
        """
        Método para obtener información del restaurante a través de la mesa.
        """
        if obj.mesa and obj.mesa.restaurante:
            restaurante = obj.mesa.restaurante
            return {
                'id': restaurante.id,
                'nombre': restaurante.nombre,
                'direccion': restaurante.direccion,
                'telefono': restaurante.telefono,
            }
        return None

    def get_mesa_numero(self, obj):
        """
        Método para obtener solo el número de la mesa.
        """
        return obj.mesa.numero if obj.mesa else None

    # --- Validación personalizada a nivel de objeto ---
    def validate(self, data):
        """
        Validación personalizada que puede involucrar múltiples campos.
        Se llama después de las validaciones de campo individuales.
        """
        # Ejemplo: Asegurarse de que la cantidad de personas no exceda la capacidad de la mesa
        # Esto requiere que 'mesa' y 'cantidad_personas' estén en 'data'
        # (lo cual puede no ser el caso si son read_only y se asignan en la vista)
        
        # Si se va a crear y se pasa la mesa directamente (no read_only)
        # mesa = data.get('mesa') 
        # cantidad_personas = data.get('cantidad_personas')
        # if mesa and cantidad_personas and cantidad_personas > mesa.capacidad:
        #     raise serializers.ValidationError(
        #         f"La cantidad de personas ({cantidad_personas}) excede la capacidad de la mesa ({mesa.capacidad})."
        #     )
        return data

# --- Serializador para Crear una Reserva (Ejemplo) ---
# Este serializador podría ser usado específicamente para la acción de crear,
# donde algunos campos son obligatorios o se manejan de forma diferente.

class CrearReservaSerializer(serializers.ModelSerializer):
    """
    Serializador específico para la creación de una reserva.
    Se enfoca en los datos de entrada del usuario.
    """
    # El usuario se obtendrá del request, no del cuerpo de la solicitud
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    # La mesa se seleccionará basándose en disponibilidad, no se pasa directamente
    # Para simplificar, podríamos pasar 'mesa_id' y validarlo, o hacerlo en la vista.
    # mesa_id = serializers.IntegerField(write_only=True) 
    
    # Campos de entrada
    restaurante_id = serializers.IntegerField(write_only=True)
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    duracion_horas = serializers.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    cantidad_personas = serializers.IntegerField(min_value=1)

    class Meta:
        model = Reserva
        fields = [
            'usuario', 'restaurante_id', 'fecha', 'hora', 'duracion_horas', 'cantidad_personas', 'nombre_cliente'
            # 'mesa_id' # Si se usara
        ]

    def validate(self, data):
        """
        Validación compleja para la creación, como verificar disponibilidad.
        Esta lógica también puede residir en la vista o en un servicio.
        """
        from datetime import datetime, timedelta
        # from .models import Mesa # Asegúrate de importar Mesa
        
        usuario = data['usuario']
        restaurante_id = data['restaurante_id']
        fecha = data['fecha']
        hora = data['hora']
        duracion_horas = float(data['duracion_horas'])
        cantidad_personas = data['cantidad_personas']
        
        # 1. Verificar que el restaurante exista
        try:
            restaurante = Restaurante.objects.get(id=restaurante_id)
        except Restaurante.DoesNotExist:
            raise serializers.ValidationError("El restaurante especificado no existe.")
            
        # 2. Encontrar mesas disponibles (capacidad suficiente)
        mesas_posibles = Mesa.objects.filter(restaurante=restaurante, capacidad__gte=cantidad_personas)
        if not mesas_posibles.exists():
             raise serializers.ValidationError("No hay mesas disponibles para esa cantidad de personas en ese restaurante.")
             
        # 3. Verificar disponibilidad horaria (lógica simplificada)
        fecha_hora_inicio = datetime.combine(fecha, hora)
        fecha_hora_fin = fecha_hora_inicio + timedelta(hours=duracion_horas)
        
        mesa_disponible = None
        for mesa in mesas_posibles:
            # Obtener reservas para esa mesa en esa fecha
            reservas_dia = Reserva.objects.filter(mesa=mesa, fecha=fecha)
            solapada = False
            for r in reservas_dia:
                inicio_r = datetime.combine(r.fecha, r.hora)
                fin_r = inicio_r + timedelta(hours=float(getattr(r, 'duracion_horas', 1)))
                if fecha_hora_inicio < fin_r and fecha_hora_fin > inicio_r:
                    solapada = True
                    break
            if not solapada:
                mesa_disponible = mesa
                break
                
        if not mesa_disponible:
            raise serializers.ValidationError("No hay mesas libres en ese horario para ese restaurante.")
            
        # Guardar la mesa encontrada en el contexto para usarla en la vista
        self.context['mesa_asignada'] = mesa_disponible
        
        return data

    def create(self, validated_data):
        """
        Crear la instancia de Reserva.
        """
        # Remover campos que no pertenecen al modelo Reserva
        validated_data.pop('restaurante_id', None)
        # La mesa se obtiene del contexto (calculado en validate)
        mesa = self.context.get('mesa_asignada')
        if not mesa:
            raise serializers.ValidationError("No se pudo asignar una mesa.")
            
        reserva = Reserva.objects.create(
            usuario=validated_data['usuario'],
            mesa=mesa,
            fecha=validated_data['fecha'],
            hora=validated_data['hora'],
            duracion_horas=validated_data['duracion_horas'],
            cantidad_personas=validated_data['cantidad_personas'],
            nombre_cliente=validated_data.get('nombre_cliente', validated_data['usuario'].username)
        )
        return reserva
