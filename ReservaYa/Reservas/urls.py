from django.urls import path
from django.http import HttpResponse

def placeholder_view(request, name=None):
    return HttpResponse(f"Vista en construcción: {name or 'pendiente'}")

urlpatterns = [
    path("quienes-somos/", lambda r: placeholder_view(r, "Quiénes Somos"), name="quienes_somos"),
    path("restaurantes/", lambda r: placeholder_view(r, "Restaurantes"), name="reservaya_rest"),
    path("restaurante/<slug:slug>/", lambda r, slug: placeholder_view(r, f"Restaurante {slug}"), name="detalle_restaurante"),
]
