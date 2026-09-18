from rest_framework import serializers

from Restaurantes.models import Restaurante
from Restaurantes.serializers import RestauranteSerializer

from .models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    restaurante_detalle = RestauranteSerializer(source="restaurante", read_only=True)
    restaurante = serializers.PrimaryKeyRelatedField(queryset=Restaurante.objects.all())
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id",
            "restaurante",
            "restaurante_detalle",
            "fecha",
            "hora",
            "numero_personas",
            "estado",
            "estado_display",
            "notas",
            "creado_en",
        ]
        read_only_fields = ["estado", "creado_en"]

    def validate_numero_personas(self, value):
        if value < 1 or value > 20:
            raise serializers.ValidationError("El número de personas debe estar entre 1 y 20.")
        return value

    def create(self, validated_data):
        validated_data["usuario"] = self.context["request"].user
        return super().create(validated_data)
