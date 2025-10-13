from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email_contacto = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    imagen_logo = models.ImageField(upload_to='restaurantes/logos/', blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='restaurantes/portadas/', blank=True, null=True)
    horario_apertura = models.TimeField(help_text="Formato HH:MM")
    horario_cierre = models.TimeField(help_text="Formato HH:MM")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Mesa(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='mesas')
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField(help_text="Número máximo de personas")
    ubicacion = models.CharField(max_length=100, blank=True, help_text="Ej: Terraza, Salón principal, Jardín")
    descripcion = models.TextField(blank=True)  # <-- Nuevo campo opcional para descripción de la mesa

    class Meta:
        ordering = ['restaurante', 'numero']
        unique_together = ('restaurante', 'numero')
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def __str__(self):
        ubicacion_str = f" ({self.ubicacion})" if self.ubicacion else ""
        return f"Mesa {self.numero}{ubicacion_str} - {self.restaurante.nombre}"


class RestauranteAdmin(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_restaurante_admin'
    )
    restaurante = models.OneToOneField(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )
    email_contacto = models.EmailField(blank=True)
    last_password_change = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrador de Restaurante"
        verbose_name_plural = "Administradores de Restaurantes"

    def __str__(self):
        return f"Admin {self.usuario.username} - {self.restaurante.nombre}"
