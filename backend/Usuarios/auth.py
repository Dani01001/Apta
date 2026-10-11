import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
