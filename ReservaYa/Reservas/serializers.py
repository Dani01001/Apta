# ReservaYa/Reservas/serializers.py
from rest_framework import serializers
# Importamos el modelo que acabamos de definir
from .models import Reserva
# También necesitamos serializadores para los modelos relacionados
# Si están en otras apps, los importamos. Asumo que Usuario está en 'Usuarios'
# y Mesa/Restaurante están en 'Restaurantes'. Ajusta las rutas según tu estructura real.
from Usuarios.models import CustomUser # Ajusta si es necesario
from Restaurantes.models import Mesa, Restaurante # Ajusta si es necesario
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Reserva, Mesa, Restaurante

# --- Serializadores para Modelos Relacionados (Opcionales pero útiles) ---

class UsuarioReservaSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para el usuario asociado a una reserva.
    Solo incluye campos esenciales.
    """
    class Meta:
        model = CustomUser
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
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nombre_cliente = serializers.CharField(required=False)

    restaurante_id = serializers.IntegerField(write_only=True)
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    duracion_horas = serializers.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    cantidad_personas = serializers.IntegerField(min_value=1)

    class Meta:
        model = Reserva
        fields = [
            'usuario', 'restaurante_id', 'fecha', 'hora', 
            'duracion_horas', 'cantidad_personas', 'nombre_cliente'
        ]

    def validate(self, data):
        usuario = data['usuario']
        restaurante_id = data['restaurante_id']
        fecha = data['fecha']
        hora = data['hora']
        duracion_horas = float(data['duracion_horas'])
        cantidad_personas = data['cantidad_personas']

        # 1️⃣ Fecha no puede ser anterior al día actual
        if fecha < timezone.localdate():
            raise serializers.ValidationError("❌ La fecha no puede ser anterior al día de hoy.")

        # 2️⃣ Duración máxima 3 horas
        if duracion_horas > 3:
            raise serializers.ValidationError("❌ La duración máxima es de 3 horas.")

        # 3️⃣ Restaurante válido
        try:
            restaurante = Restaurante.objects.get(id=restaurante_id)
        except Restaurante.DoesNotExist:
            raise serializers.ValidationError("❌ Restaurante no existe.")

        # 4️⃣ Mesas disponibles según cantidad de personas
        mesas_posibles = Mesa.objects.filter(restaurante=restaurante, capacidad__gte=cantidad_personas)
        if not mesas_posibles.exists():
            raise serializers.ValidationError("❌ No hay mesas disponibles para esa cantidad de personas.")

        # 5️⃣ Verificar solapamiento horario
        fecha_hora_inicio = datetime.combine(fecha, hora)
        fecha_hora_fin = fecha_hora_inicio + timedelta(hours=duracion_horas)
        mesa_disponible = None

        for mesa in mesas_posibles:
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
            raise serializers.ValidationError("❌ No hay mesas libres en ese horario para ese restaurante.")

        # Guardar la mesa asignada en el contexto
        self.context['mesa_asignada'] = mesa_disponible
        return data

    def create(self, validated_data):
        mesa = self.context.get('mesa_asignada')
        if not mesa:
            raise serializers.ValidationError("No se pudo asignar una mesa.")

        # Generar nombre del cliente si no se pasa
        nombre_cliente = validated_data.get('nombre_cliente') or validated_data['usuario'].username

        reserva = Reserva.objects.create(
            usuario=validated_data['usuario'],
            mesa=mesa,
            fecha=validated_data['fecha'],
            hora=validated_data['hora'],
            duracion_horas=validated_data['duracion_horas'],
            cantidad_personas=validated_data['cantidad_personas'],
            nombre_cliente=nombre_cliente,
            estado='pendiente'  # ✅ Reserva siempre inicia como pendiente
        )
        return reserva
