from django.utils import timezone
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

    def validate_fecha(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError("La fecha de la reserva no puede ser en el pasado.")
        return value

    def validate(self, attrs):
        restaurante = attrs.get("restaurante") or getattr(self.instance, "restaurante", None)
        hora = attrs.get("hora") or getattr(self.instance, "hora", None)
        numero_personas = attrs.get("numero_personas") or getattr(
            self.instance, "numero_personas", None
        )

        if restaurante and hora is not None:
            if not (restaurante.hora_apertura <= hora <= restaurante.hora_cierre):
                raise serializers.ValidationError(
                    {
                        "hora": (
                            f"{restaurante.nombre} atiende de "
                            f"{restaurante.hora_apertura.strftime('%H:%M')} a "
                            f"{restaurante.hora_cierre.strftime('%H:%M')}."
                        )
                    }
                )

        if restaurante and numero_personas and numero_personas > restaurante.capacidad:
            raise serializers.ValidationError(
                {
                    "numero_personas": (
                        f"{restaurante.nombre} tiene una capacidad máxima de "
                        f"{restaurante.capacidad} personas por mesa."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data["usuario"] = self.context["request"].user
        return super().create(validated_data)
