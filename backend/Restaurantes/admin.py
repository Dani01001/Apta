from django.contrib import admin

from .models import Restaurante


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "ciudad", "categoria", "rango_precio", "calificacion", "activo"]
    list_filter = ["categoria", "ciudad", "rango_precio", "activo"]
    search_fields = ["nombre", "ciudad"]
    prepopulated_fields = {"slug": ("nombre",)}
