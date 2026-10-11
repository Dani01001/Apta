from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Reserva
from .serializers import ReservaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related("restaurante")

    ESTADOS_FINALES = (Reserva.Estado.CANCELADA, Reserva.Estado.COMPLETADA)

    def partial_update(self, request, *args, **kwargs):
        if self.get_object().estado in self.ESTADOS_FINALES:
            return Response(
                {"detail": "Esta reserva ya no se puede modificar."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().estado in self.ESTADOS_FINALES:
            return Response(
                {"detail": "Esta reserva queda en el historial y no se puede eliminar."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado in self.ESTADOS_FINALES:
            return Response(
                {"detail": "Esta reserva ya no se puede cancelar."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reserva.estado = Reserva.Estado.CANCELADA
        reserva.save(update_fields=["estado"])
        return Response(ReservaSerializer(reserva).data)
