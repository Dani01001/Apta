from django.contrib.auth.models import User
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
        self.assertIn("refresh", respuesta.data)
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
