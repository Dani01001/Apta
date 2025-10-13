from django.urls import path, include
from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("perfil/", views.profile_view, name="profile"),
    path("perfil/editar/", views.profile_edit_view, name="profile_edit"),
    path("pagina_priv/", views.paginapriv, name="pagina_priv"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard_restaurante/", views.panel_restaurante, name="dashboard_restaurante"),
    path("dashboard_usuario/", views.dashboard, name="dashboard_usuario"),
    # path("perfil/reservas/", views.mis_reservas_view, name="mis_reservas"),
    
    # Login con Google (django-allauth)
    path("accounts/", include("allauth.urls")),
]