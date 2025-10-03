from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def user_avatar_upload_to(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    ROLE_USER = 'user'
    ROLE_RESTAURANT = 'restaurant_admin'
    ROLE_CHOICES = [
        (ROLE_USER, 'Usuario'),
        (ROLE_RESTAURANT, 'Administrador Restaurante'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_USER)
    perfil_imagen = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True)
    is_restaurant_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email'] # email obligatorio

    def get_initial(self):
        base = (self.get_full_name() or self.username or (self.email or ''))
        base = base.strip()
        return base[0].upper() if base else 'U'

    def is_restaurant_admin(self):
        return self.role == self.ROLE_RESTAURANT
    
