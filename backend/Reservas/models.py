from django.conf import settings
from django.db import models

from Restaurantes.models import Restaurante


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"
        COMPLETADA = "completada", "Completada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas"
    )
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="reservas"
    )
    fecha = models.DateField()
    hora = models.TimeField()
    numero_personas = models.PositiveSmallIntegerField(default=2)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    notas = models.CharField(max_length=280, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-hora"]

    def __str__(self):
        return f"{self.usuario} en {self.restaurante} el {self.fecha}"
