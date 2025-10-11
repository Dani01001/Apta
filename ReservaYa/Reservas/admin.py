from django.contrib import admin
from .models import Reserva
from import_export.admin import ImportExportActionModelAdmin

@admin.register(Reserva)
class ReservaAdmin(ImportExportActionModelAdmin):
    pass
