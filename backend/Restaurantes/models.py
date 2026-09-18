from django.db import models


class Restaurante(models.Model):
    class Categoria(models.TextChoices):
        PARAGUAYA = "paraguaya", "Comida Paraguaya"
        PARRILLA = "parrilla", "Parrilla y Asado"
        INTERNACIONAL = "internacional", "Internacional"
        MARISCOS = "mariscos", "Mariscos y Pescados"
        VEGETARIANA = "vegetariana", "Vegetariana"
        ITALIANA = "italiana", "Italiana"
        JAPONESA = "japonesa", "Japonesa"
        CAFETERIA = "cafeteria", "Cafetería y Confitería"

    class RangoPrecio(models.TextChoices):
        ECONOMICO = "$", "Económico"
        MODERADO = "$$", "Moderado"
        ALTO = "$$$", "Alto"
        PREMIUM = "$$$$", "Premium"

    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    ciudad = models.CharField(max_length=80)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    rango_precio = models.CharField(
        max_length=4, choices=RangoPrecio.choices, default=RangoPrecio.MODERADO
    )
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    capacidad = models.PositiveIntegerField(default=40)
    hora_apertura = models.TimeField(default="12:00")
    hora_cierre = models.TimeField(default="22:00")
    imagen_url = models.URLField()
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-destacado", "-calificacion"]

    def __str__(self):
        return self.nombre
