from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Perfil


class RegistroTests(APITestCase):
    def test_registro_crea_usuario_perfil_y_devuelve_tokens(self):
        respuesta = self.client.post(
            "/api/usuarios/registro/",
            {
                "username": "nueva.usuaria",
                "email": "nueva@example.com",
                "first_name": "Nueva",
                "last_name": "Usuaria",
                "password": "ContraseñaSegura123",
                "telefono": "+595 981 000 000",
            },
        )
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", respuesta.data)
        self.assertIn("reservaya_refresh", respuesta.cookies)
        usuario = User.objects.get(username="nueva.usuaria")
        self.assertTrue(Perfil.objects.filter(usuario=usuario).exists())

    def test_registro_rechaza_username_duplicado(self):
        User.objects.create_user(username="demo", password="Demo1234")
        respuesta = self.client.post(
            "/api/usuarios/registro/",
            {
                "username": "demo",
                "email": "otro@example.com",
                "first_name": "Otro",
                "last_name": "Usuario",
                "password": "ContraseñaSegura123",
            },
        )
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", respuesta.data)

    def test_registro_rechaza_contrasena_debil(self):
        respuesta = self.client.post(
            "/api/usuarios/registro/",
            {
                "username": "usuario.debil",
                "email": "debil@example.com",
                "first_name": "Usuario",
                "last_name": "Débil",
                "password": "12345678",
            },
        )
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="demo", password="Demo1234", email="demo@apta.com.py"
        )
        Perfil.objects.create(usuario=self.usuario, telefono="+595 981 111 222")

    def test_login_devuelve_tokens_y_datos_de_usuario(self):
        respuesta = self.client.post(
            "/api/usuarios/login/", {"username": "demo", "password": "Demo1234"}
        )
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertIn("access", respuesta.data)
        self.assertEqual(respuesta.data["usuario"]["username"], "demo")

    def test_login_rechaza_contrasena_incorrecta(self):
        respuesta = self.client.post(
            "/api/usuarios/login/", {"username": "demo", "password": "incorrecta"}
        )
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)


class PerfilActualTests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="demo", password="Demo1234")
        Perfil.objects.create(usuario=self.usuario, telefono="+595 981 111 222")

    def test_me_requiere_autenticacion(self):
        respuesta = self.client.get("/api/usuarios/me/")
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_devuelve_datos_del_usuario_autenticado(self):
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.get("/api/usuarios/me/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data["username"], "demo")

    def test_me_permite_actualizar_el_telefono(self):
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.patch(
            "/api/usuarios/me/", {"perfil": {"telefono": "+595 981 999 999"}}, format="json"
        )
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.perfil.telefono, "+595 981 999 999")


class LimiteDeIntentosTests(APITestCase):
    def setUp(self):
        cache.clear()
        User.objects.create_user(username="demo", password="Demo1234")

    def tearDown(self):
        cache.clear()

    def test_bloquea_el_login_despues_de_muchos_intentos(self):
        for _ in range(10):
            self.client.post("/api/usuarios/login/", {"username": "demo", "password": "incorrecta"})
        respuesta = self.client.post("/api/usuarios/login/", {"username": "demo", "password": "Demo1234"})
        self.assertEqual(respuesta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class CookieRefrescoTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.usuario = User.objects.create_user(username="demo", password="Demo1234")
        Perfil.objects.create(usuario=self.usuario, telefono="+595 981 111 222")

    def tearDown(self):
        cache.clear()

    def _login(self):
        return self.client.post("/api/usuarios/login/", {"username": "demo", "password": "Demo1234"})

    def test_login_pone_el_refresco_en_cookie_httponly_y_no_en_el_cuerpo(self):
        respuesta = self._login()
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertNotIn("refresh", respuesta.data)
        cookie = respuesta.cookies["reservaya_refresh"]
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["path"], "/api/usuarios/")
        self.assertEqual(cookie["samesite"], "Lax")

    def test_registro_pone_el_refresco_en_cookie(self):
        respuesta = self.client.post(
            "/api/usuarios/registro/",
            {
                "username": "otra.persona",
                "email": "otra@example.com",
                "first_name": "Otra",
                "last_name": "Persona",
                "password": "ContraseñaSegura123",
            },
        )
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("refresh", respuesta.data)
        self.assertIn("reservaya_refresh", respuesta.cookies)

    def test_renovar_con_cookie_devuelve_access_y_usuario_y_rota_la_cookie(self):
        anterior = self._login().cookies["reservaya_refresh"].value
        respuesta = self.client.post("/api/usuarios/token/refresh/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertIn("access", respuesta.data)
        self.assertEqual(respuesta.data["usuario"]["username"], "demo")
        self.assertNotEqual(respuesta.cookies["reservaya_refresh"].value, anterior)

    def test_el_refresco_rotado_no_se_puede_reusar(self):
        anterior = self._login().cookies["reservaya_refresh"].value
        self.client.post("/api/usuarios/token/refresh/")
        self.client.cookies["reservaya_refresh"] = anterior
        respuesta = self.client.post("/api/usuarios/token/refresh/")
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_renovar_sin_cookie_responde_401(self):
        respuesta = self.client.post("/api/usuarios/token/refresh/")
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_renovar_rechaza_un_origen_ajeno(self):
        self._login()
        respuesta = self.client.post("/api/usuarios/token/refresh/", HTTP_ORIGIN="https://sitio-malicioso.example")
        self.assertEqual(respuesta.status_code, status.HTTP_403_FORBIDDEN)

    def test_renovar_acepta_el_origen_del_frontend(self):
        self._login()
        respuesta = self.client.post("/api/usuarios/token/refresh/", HTTP_ORIGIN="http://localhost:3000")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)

    def test_logout_invalida_el_refresco_y_borra_la_cookie(self):
        refresco = self._login().cookies["reservaya_refresh"].value
        respuesta = self.client.post("/api/usuarios/logout/")
        self.assertEqual(respuesta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(respuesta.cookies["reservaya_refresh"].value, "")
        self.client.cookies["reservaya_refresh"] = refresco
        respuesta = self.client.post("/api/usuarios/token/refresh/")
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)
