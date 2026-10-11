from urllib.parse import urlparse

from django.conf import settings

REFRESH_COOKIE = "reservaya_refresh"
REFRESH_COOKIE_PATH = "/api/usuarios/"


def poner_cookie_refresh(respuesta, refresh):
    # El token de refresco viaja solo en una cookie HttpOnly: el JS del navegador no lo puede leer
    respuesta.set_cookie(
        REFRESH_COOKIE,
        str(refresh),
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path=REFRESH_COOKIE_PATH,
        secure=not settings.DEBUG,
        httponly=True,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
    )
    return respuesta


def borrar_cookie_refresh(respuesta):
    respuesta.delete_cookie(
        REFRESH_COOKIE, path=REFRESH_COOKIE_PATH, samesite=settings.REFRESH_COOKIE_SAMESITE
    )
    return respuesta


def origen_permitido(request):
    # Defensa contra CSRF en las rutas que usan la cookie: si el navegador manda Origin,
    # tiene que ser el propio backend o uno de los orígenes del frontend
    origen = request.headers.get("Origin")
    if not origen:
        return True
    if origen in settings.CORS_ALLOWED_ORIGINS:
        return True
    return urlparse(origen).netloc == request.get_host()
