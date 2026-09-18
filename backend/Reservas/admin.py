from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "restaurante", "fecha", "hora", "numero_personas", "estado"]
    list_filter = ["estado", "fecha"]
    search_fields = ["usuario__username", "restaurante__nombre"]
