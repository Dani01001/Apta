from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ["usuario", "telefono", "creado_en"]
    search_fields = ["usuario__username", "usuario__email"]
