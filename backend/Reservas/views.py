from rest_framework import permissions, viewsets
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

    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        reserva.estado = Reserva.Estado.CANCELADA
        reserva.save(update_fields=["estado"])
        return Response(ReservaSerializer(reserva).data)
