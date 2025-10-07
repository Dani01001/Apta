# ReservaYa/Reservas/urls.py
from django.urls import path
from . import views

app_name = 'reservas' # Namespace para las URLs

urlpatterns = [
    path('', views.reservas_view, name='reservas'),
    # === APIs ===
    path('api/crear/', views.crear_reserva_api, name='api_crear_reserva'),
    path('api/mis_reservas/', views.mis_reservas_api, name='api_mis_reservas'),
    path('api/<int:reserva_id>/cancelar/', views.cancelar_reserva_api, name='api_cancelar_reserva'),
    path('api/<int:reserva_id>/editar/', views.editar_reserva_api, name='api_editar_reserva'),
    path('api/restaurante/<int:restaurante_id>/mesas_disponibles/', views.obtener_mesas_disponibles_api, name='api_mesas_disponibles'),
    
    # === Vistas HTML (opcionales) ===
    # path('formulario/', views.formulario_reserva_html, name='formulario_reserva'),
    # path('mis_reservas/', views.mis_reservas_html, name='mis_reservas_html'),
]
