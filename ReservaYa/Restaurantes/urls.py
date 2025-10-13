# ReservaYa/restaurantes/urls.py
from django.urls import path
from . import views

app_name = "restaurantes"

urlpatterns = [
    # === VISTAS PÚBLICAS (Para Clientes y Visitantes) ===
    path('', views.lista_restaurantes, name='lista_restaurantes'),
    path('<slug:slug>/', views.detalle_restaurante, name='detalle_restaurante'),

    # === PANEL DE ADMINISTRACIÓN DEL RESTAURANTE ===
    # (Requieren inicio de sesión y permisos de RestauranteAdmin)
    path('admin/', views.panel_admin_restaurante, name='panel_admin_restaurante'),
    path('admin/restaurante/', views.gestionar_restaurante, name='gestionar_restaurante'),
    path('admin/mesas/', views.gestionar_mesas, name='gestionar_mesas'),
    # Vista para eliminar una mesa (por ejemplo, para llamadas AJAX o formularios POST)
    path('admin/mesas/<int:mesa_id>/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),
    path('admin/reservas/', views.ver_reservas_restaurante, name='ver_reservas_restaurante'),
    path('admin/restaurante/actualizar_estado/<int:reserva_id>/', views.actualizar_estado_reserva, name='actualizar_estado_reserva')

    # === APIs (para integración con frontend o otras apps) ===
    # Ejemplo: Obtener mesas disponibles (puede ser consumida por JS o la app 'reservas')
    # Asegúrate de que esta vista exista en views.py
    # path('api/<int:restaurante_id>/mesas/disponibles/', views.api_obtener_mesas_disponibles, name='api_obtener_mesas_disponibles'),
]
