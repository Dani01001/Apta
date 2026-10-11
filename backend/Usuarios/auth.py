import logging

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .cookies import REFRESH_COOKIE, borrar_cookie_refresh, origen_permitido, poner_cookie_refresh
from .serializers import UsuarioSerializer

registro = logging.getLogger("reservaya.seguridad")


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            registro.warning("Login fallido para el usuario %r", attrs.get(self.username_field, "")[:150])
            raise
        registro.info("Login correcto del usuario id=%s", self.user.pk)
        data["usuario"] = UsuarioSerializer(self.user).data
        return data


class LoginView(TokenObtainPairView):
    throttle_scope = "auth"
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        respuesta = super().post(request, *args, **kwargs)
        if respuesta.status_code == status.HTTP_200_OK:
            refresh = respuesta.data.pop("refresh")
            poner_cookie_refresh(respuesta, refresh)
        return respuesta


class RenovarTokenView(APIView):
    """Entrega un token de acceso nuevo a partir de la cookie de refresco y la rota."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        if not origen_permitido(request):
            registro.warning("Renovación rechazada por origen no permitido: %r", request.headers.get("Origin"))
            return Response({"detail": "Origen no permitido."}, status=status.HTTP_403_FORBIDDEN)
        refresh = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh:
            return Response({"detail": "Sin sesión."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TokenRefreshSerializer(data={"refresh": refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            return Response({"detail": "La sesión venció."}, status=status.HTTP_401_UNAUTHORIZED)
        datos = serializer.validated_data
        usuario_id = RefreshToken(datos.get("refresh", refresh), verify=False).payload.get("user_id")
        usuario = get_user_model().objects.filter(pk=usuario_id, is_active=True).first()
        if usuario is None:
            return Response({"detail": "La sesión venció."}, status=status.HTTP_401_UNAUTHORIZED)
        respuesta = Response({"access": datos["access"], "usuario": UsuarioSerializer(usuario).data})
        if "refresh" in datos:
            poner_cookie_refresh(respuesta, datos["refresh"])
        return respuesta


class LogoutView(APIView):
    """Invalida el token de refresco de la cookie y la borra."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        if not origen_permitido(request):
            return Response({"detail": "Origen no permitido."}, status=status.HTTP_403_FORBIDDEN)
        refresh = request.COOKIES.get(REFRESH_COOKIE)
        if refresh:
            try:
                RefreshToken(refresh).blacklist()
            except TokenError:
                pass
        return borrar_cookie_refresh(Response(status=status.HTTP_204_NO_CONTENT))
