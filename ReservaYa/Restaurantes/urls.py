from django.urls import path
from . import views

app_name = 'restaurantes'

urlpatterns = [
    # Panel principal de gestión
    path('gestionar/', views.gestionar_restaurante, name='gestionar_restaurante'),

    # AJAX: actualizar estado de reserva
    path('gestionar/actualizar_estado/<int:reserva_id>/', views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    path('gestionar/actualizar_estado_multiple/', views.actualizar_estado_multiple, name='actualizar_estado_multiple'),

    # AJAX: mesas
    path('gestionar/agregar_mesa_ajax/', views.agregar_mesa_ajax, name='agregar_mesa_ajax'),
    path('gestionar/editar_mesa_ajax/<int:mesa_id>/', views.editar_mesa_ajax, name='editar_mesa_ajax'),
    path('gestionar/eliminar_mesa/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa_ajax'),

    # Vistas públicas
    path('', views.lista_restaurantes, name='lista_restaurantes'),
    path('<slug:slug>/', views.detalle_restaurante, name='detalle_restaurante'),
]
