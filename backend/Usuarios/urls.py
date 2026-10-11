from django.urls import path

from .views import PerfilActualView, RegistroView
from .auth import LoginView, LogoutView, RenovarTokenView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="usuarios-registro"),
    path("login/", LoginView.as_view(), name="usuarios-login"),
    path("token/refresh/", RenovarTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="usuarios-logout"),
    path("me/", PerfilActualView.as_view(), name="usuarios-me"),
]
