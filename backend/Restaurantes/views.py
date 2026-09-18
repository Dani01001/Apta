from rest_framework import viewsets

from .models import Restaurante
from .serializers import RestauranteSerializer


class RestauranteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurante.objects.filter(activo=True)
    serializer_class = RestauranteSerializer
    lookup_field = "slug"
    filterset_fields = ["categoria", "ciudad", "rango_precio"]
    search_fields = ["nombre", "descripcion", "ciudad"]
    ordering_fields = ["calificacion", "nombre"]
