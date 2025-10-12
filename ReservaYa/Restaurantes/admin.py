# Ejemplo de cómo podría ser tu archivo admin.py después
from django.contrib import admin
from .models import Restaurante, Mesa, RestauranteAdmin # Asegúrate de importar tus modelos
from import_export.admin import ImportExportActionModelAdmin

@admin.register(Restaurante)
class RestauranteAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(Mesa)
class MesaAdmin(ImportExportActionModelAdmin):
    pass