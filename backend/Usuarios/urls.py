from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PerfilActualView, RegistroView
from .auth import LoginView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="usuarios-registro"),
    path("login/", LoginView.as_view(), name="usuarios-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", PerfilActualView.as_view(), name="usuarios-me"),
]
