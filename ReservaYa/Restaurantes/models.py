# ReservaYa/restaurantes/models.py
from django.db import models
from django.conf import settings # Para referenciar el modelo de usuario personalizado
from django.contrib.auth.hashers import make_password, check_password # Para manejar la contraseña del admin
from django.utils.text import slugify

class Restaurante(models.Model):
    """
    Representa un restaurante en la plataforma.
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="Usado en URLs amigables.") # Opcional, útil para URLs
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email_contacto = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    # Imágenes
    imagen_logo = models.ImageField(upload_to='restaurantes/logos/', blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='restaurantes/portadas/', blank=True, null=True)
    # Horarios (se podrían hacer más sofisticados con un modelo separado)
    horario_apertura = models.TimeField(help_text="Formato HH:MM")
    horario_cierre = models.TimeField(help_text="Formato HH:MM")
    # Otros metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True, help_text="Indica si el restaurante está disponible para reservas.")

    class Meta:
        ordering = ['nombre'] # Ordenar por nombre por defecto
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """
        Override save para generar el slug automáticamente si no se proporciona.
        """
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    # @property
    # def get_horario_formateado(self):
    #     return f"{self.horario_apertura.strftime('%H:%M')} - {self.horario_cierre.strftime('%H:%M')}"


class Mesa(models.Model):
    """
    Representa una mesa dentro de un restaurante.
    """
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='mesas')
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField(help_text="Número máximo de personas que puede sentar la mesa.")
    # Opcional: ubicación dentro del restaurante
    ubicacion = models.CharField(max_length=100, blank=True, help_text="Ej: Terraza, Salón principal, Jardín")

    class Meta:
        ordering = ['restaurante', 'numero'] # Ordenar por restaurante y luego por número de mesa
        unique_together = ('restaurante', 'numero') # No puede haber dos mesas con el mismo número en el mismo restaurante
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def __str__(self):
        ubicacion_str = f" ({self.ubicacion})" if self.ubicacion else ""
        return f"Mesa {self.numero}{ubicacion_str} - {self.restaurante.nombre}"


# Importación diferida para evitar problemas de dependencias circulares
# Se importará dentro de la función donde se necesite.
# from django.contrib.auth import get_user_model

class RestauranteAdmin(models.Model):
    """
    Representa un usuario administrador asociado a un restaurante específico.
    Este modelo permite que un usuario (del modelo AUTH_USER_MODEL) tenga permisos
    de administración sobre un restaurante.
    NOTA: Este modelo asume que el usuario base ya existe (por ejemplo, en la app 'usuarios').
    """
    # Relación Uno a Uno con el modelo de usuario personalizado
    # Usamos settings.AUTH_USER_MODEL para referenciarlo dinámicamente
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_restaurante_admin' # Permite acceder desde User: user.perfil_restaurante_admin
    )
    # Relación con el restaurante que administra
    restaurante = models.OneToOneField(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='admin_profile' # Permite acceder desde Restaurante: restaurante.admin_profile
    )
    # Información de contacto específica del rol de admin (opcional, puede usar la del usuario base)
    email_contacto = models.EmailField(blank=True, help_text="Email específico para administración del restaurante.")

    # Control de cambios (ejemplo)
    last_password_change = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Administrador de Restaurante"
        verbose_name_plural = "Administradores de Restaurantes"

    def __str__(self):
        return f"Admin {self.usuario.username} - {self.restaurante.nombre}"

    def save(self, *args, **kwargs):
        """
        Puedes agregar lógica personalizada aquí si es necesario antes de guardar.
        Por ejemplo, enviar una notificación al crear un nuevo admin.
        """
        super().save(*args, **kwargs)

# Opcional: Si necesitas un modelo completamente independiente para admins de restaurante
# (no basado en el modelo de usuario estándar), puedes definirlo así:
# class RestauranteAdminIndependiente(models.Model):
#     """
#     Modelo para un administrador de restaurante completamente independiente.
#     Úsalo solo si el modelo de usuario estándar no es adecuado o deseas una autenticación separada.
#     ADVERTENCIA: Esto complica significativamente la autenticación y autorización.
#     """
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128) # Almacenará el hash de la contraseña
#     restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='admins_independientes')
#
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#
#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)
#
#     def __str__(self):
#         return f"{self.username} (Admin de {self.restaurante.nombre})"
