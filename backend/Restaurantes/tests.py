from rest_framework import status
from rest_framework.test import APITestCase

from .models import Restaurante


class RestauranteModelTests(APITestCase):
    def test_str_devuelve_el_nombre(self):
        restaurante = Restaurante.objects.create(
            nombre="Tierra Colorada",
            slug="tierra-colorada",
            descripcion="Cocina paraguaya de autor.",
            categoria=Restaurante.Categoria.PARAGUAYA,
            ciudad="Asunción",
            direccion="Carmelitas",
            imagen_url="https://picsum.photos/seed/tierra-colorada/800/600",
        )
        self.assertEqual(str(restaurante), "Tierra Colorada")


class RestauranteApiTests(APITestCase):
    def setUp(self):
        self.activo = Restaurante.objects.create(
            nombre="La Cabrera Asunción",
            slug="la-cabrera-asuncion",
            descripcion="Parrilla porteña.",
            categoria=Restaurante.Categoria.PARRILLA,
            ciudad="Asunción",
            direccion="Villa Morra",
            rango_precio=Restaurante.RangoPrecio.PREMIUM,
            calificacion=4.8,
            imagen_url="https://picsum.photos/seed/la-cabrera/800/600",
            activo=True,
        )
        self.inactivo = Restaurante.objects.create(
            nombre="Cerrado Definitivamente",
            slug="cerrado-definitivamente",
            descripcion="Local dado de baja.",
            categoria=Restaurante.Categoria.INTERNACIONAL,
            ciudad="Asunción",
            direccion="Centro",
            imagen_url="https://picsum.photos/seed/cerrado/800/600",
            activo=False,
        )

    def test_listado_excluye_restaurantes_inactivos(self):
        respuesta = self.client.get("/api/restaurantes/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        slugs = [item["slug"] for item in respuesta.data["results"]]
        self.assertIn(self.activo.slug, slugs)
        self.assertNotIn(self.inactivo.slug, slugs)

    def test_filtro_por_categoria(self):
        respuesta = self.client.get("/api/restaurantes/?categoria=parrilla")
        slugs = [item["slug"] for item in respuesta.data["results"]]
        self.assertEqual(slugs, [self.activo.slug])

    def test_detalle_por_slug(self):
        respuesta = self.client.get(f"/api/restaurantes/{self.activo.slug}/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data["nombre"], self.activo.nombre)

    def test_detalle_inexistente_devuelve_404(self):
        respuesta = self.client.get("/api/restaurantes/no-existe/")
        self.assertEqual(respuesta.status_code, status.HTTP_404_NOT_FOUND)

    def test_solo_lectura_no_permite_crear_a_un_visitante_anonimo(self):
        # IsAuthenticatedOrReadOnly corta el paso antes de resolver el método:
        # un anónimo recibe 401, no 405, porque nunca llega a comprobar que
        # el ViewSet ni siquiera define un handler para POST.
        respuesta = self.client.post(
            "/api/restaurantes/", {"nombre": "Nuevo", "slug": "nuevo"}
        )
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_solo_lectura_no_permite_crear_a_un_usuario_autenticado(self):
        from django.contrib.auth.models import User

        usuario = User.objects.create_user(username="demo", password="Demo1234")
        self.client.force_authenticate(usuario)
        respuesta = self.client.post(
            "/api/restaurantes/", {"nombre": "Nuevo", "slug": "nuevo"}
        )
        self.assertEqual(respuesta.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
