from django.db import models


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
# Create your models here.
