from django.urls import path, include
from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("perfil/", views.profile_view, name="profile"),
    path("perfil/editar/", views.profile_edit_view, name="profile_edit"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard_restaurante/", views.panel_restaurante, name="dashboard_restaurante"),
    path("dashboard_usuario/", views.dashboard, name="dashboard_usuario"),

    # Login con Google (django-allauth)
    path("accounts/", include("allauth.urls")),
]