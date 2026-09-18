from rest_framework import serializers

from .models import Restaurante


class RestauranteSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source="get_categoria_display", read_only=True)
    rango_precio_display = serializers.CharField(
        source="get_rango_precio_display", read_only=True
    )

    class Meta:
        model = Restaurante
        fields = [
            "id",
            "nombre",
            "slug",
            "descripcion",
            "categoria",
            "categoria_display",
            "ciudad",
            "direccion",
            "telefono",
            "rango_precio",
            "rango_precio_display",
            "calificacion",
            "capacidad",
            "hora_apertura",
            "hora_cierre",
            "imagen_url",
            "destacado",
        ]
