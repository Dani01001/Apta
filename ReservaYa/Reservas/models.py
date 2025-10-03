# ReservaYa/Reservas/models.py
from django.db import models
from django.conf import settings  # Para referenciar AUTH_USER_MODEL
# Importa los modelos de otras apps
# Ajusta estas rutas según dónde hayas definido Restaurante y Mesa.
# Basándome en tu mensaje anterior, parecen estar en 'Restaurantes'.
from Restaurantes.models import Mesa, Restaurante

class Reserva(models.Model):
    """
    Representa una reserva realizada por un usuario para una mesa específica
    en un restaurante, en una fecha y hora determinadas.
    """
    # Relación con el usuario que hace la reserva
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Apunta a 'Usuarios.Usuario'
        on_delete=models.CASCADE,  # Si se borra el usuario, se borran sus reservas
        related_name='reservas'     # Permite acceder desde User: user.reservas.all()
    )
    
    # Relación con la mesa reservada
    mesa = models.ForeignKey(
        Mesa,                       # Apunta al modelo Mesa de 'Restaurantes'
        on_delete=models.CASCADE,  # Si se borra la mesa, se borra la reserva
        related_name='reservas'     # Permite acceder desde Mesa: mesa.reservas.all()
    )
    
    # Información de la reserva
    nombre_cliente = models.CharField(max_length=100, help_text="Nombre con el que se hace la reserva.")
    fecha = models.DateField(help_text="Fecha de la reserva.")
    hora = models.TimeField(help_text="Hora de inicio de la reserva.")
    
    # Duración de la reserva (opcional pero útil para verificar disponibilidad)
    duracion_horas = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=1.0,
        help_text="Duración estimada de la reserva en horas (e.g., 1.5)."
    )
    
    cantidad_personas = models.PositiveIntegerField(help_text="Número de personas para la reserva.")
    
    # Estado de la reserva (puede ser útil para filtros)
    ESTADO_OPCIONES = [
        ('confirmada', 'Confirmada'),
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(
        max_length=15, 
        choices=ESTADO_OPCIONES, 
        default='confirmada',
        help_text="Estado actual de la reserva."
    )
    
    # Código único para la reserva (opcional, útil para búsquedas)
    codigo_reserva = models.CharField(max_length=20, unique=True, blank=True, help_text="Código único de la reserva.")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora en que se creó la reserva.")
    fecha_actualizacion = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización.")

    class Meta:
        ordering = ['-fecha', 'hora'] # Ordenar por fecha descendente, luego por hora
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        # Evitar reservas duplicadas para el mismo usuario, mesa, fecha y hora
        unique_together = ('usuario', 'mesa', 'fecha', 'hora') 

    def __str__(self):
        return f"Reserva de {self.nombre_cliente} (Mesa {self.mesa.numero}) el {self.fecha} a las {self.hora}"

    def save(self, *args, **kwargs):
        """
        Override save para generar el codigo_reserva si no se proporciona.
        """
        if not self.codigo_reserva:
            # Generar un código único simple (puedes hacerlo más robusto)
            import uuid
            self.codigo_reserva = f"RV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def restaurante(self):
        """Obtiene el restaurante asociado a través de la mesa."""
        return self.mesa.restaurante

    @property
    def fecha_hora_fin(self):
        """Calcula la fecha y hora de finalización de la reserva."""
        from datetime import datetime, timedelta
        fecha_hora_inicio = datetime.combine(self.fecha, self.hora)
        # Convierte duracion_horas a float para timedelta
        duracion_float = float(self.duracion_horas) 
        return fecha_hora_inicio + timedelta(hours=duracion_float)

    def clean(self):
        """
        Validaciones personalizadas del modelo.
        Se llama durante la validación del formulario o serializer.
        """
        from django.core.exceptions import ValidationError
        # Validar que la cantidad de personas no exceda la capacidad de la mesa
        if self.cantidad_personas and self.mesa:
            if self.cantidad_personas > self.mesa.capacidad:
                raise ValidationError(
                    f"La cantidad de personas ({self.cantidad_personas}) excede la capacidad de la mesa ({self.mesa.capacidad})."
                )
        # Validar que la fecha no sea en el pasado (ejemplo)
        # from django.utils import timezone
        # if self.fecha and self.fecha < timezone.now().date():
        #     raise ValidationError("La fecha de la reserva no puede ser en el pasado.")

    # Puedes agregar más métodos de utilidad aquí, por ejemplo:
    # def esta_activa(self):
    #     from django.utils import timezone
    #     ahora = timezone.now()
    #     return self.estado == 'confirmada' and \
    #            self.fecha >= ahora.date() and \
    #            not (self.fecha == ahora.date() and self.hora < ahora.time())
