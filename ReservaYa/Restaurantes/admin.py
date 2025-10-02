# Ejemplo de cómo podría ser tu archivo admin.py después
from django.contrib import admin
from .models import Restaurante, Mesa, RestauranteAdmin # Asegúrate de importar tus modelos

admin.site.register(Restaurante)
admin.site.register(Mesa)# Solo si este modelo existe y quieres registrarlo AQUÍ
admin.site.register(RestauranteAdmin) # Solo si este modelo existe y quieres registrarlo AQUÍ