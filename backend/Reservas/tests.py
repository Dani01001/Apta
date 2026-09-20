from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from Restaurantes.models import Restaurante

from .models import Reserva


class ReservaApiTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="demo", password="Demo1234")
        self.otro_usuario = User.objects.create_user(username="otra", password="Demo1234")
        self.restaurante = Restaurante.objects.create(
            nombre="Tierra Colorada",
            slug="tierra-colorada",
            descripcion="Cocina paraguaya de autor.",
            categoria=Restaurante.Categoria.PARAGUAYA,
            ciudad="Asunción",
            direccion="Carmelitas",
            capacidad=40,
            hora_apertura="12:00",
            hora_cierre="22:00",
            imagen_url="https://picsum.photos/seed/tierra-colorada/800/600",
        )
        self.manana = timezone.localdate() + timedelta(days=1)

    def _payload(self, **overrides):
        payload = {
            "restaurante": self.restaurante.id,
            "fecha": str(self.manana),
            "hora": "20:00",
            "numero_personas": 4,
            "notas": "",
        }
        payload.update(overrides)
        return payload


class CrearReservaTests(ReservaApiTestCase):
    def test_requiere_autenticacion(self):
        respuesta = self.client.post("/api/reservas/", self._payload())
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crea_reserva_valida_en_estado_pendiente(self):
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.post("/api/reservas/", self._payload())
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(respuesta.data["estado"], Reserva.Estado.PENDIENTE)
        self.assertEqual(Reserva.objects.get().usuario, self.usuario)

    def test_rechaza_fecha_en_el_pasado(self):
        self.client.force_authenticate(self.usuario)
        ayer = timezone.localdate() - timedelta(days=1)
        respuesta = self.client.post("/api/reservas/", self._payload(fecha=str(ayer)))
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fecha", respuesta.data)

    def test_rechaza_horario_fuera_de_atencion(self):
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.post("/api/reservas/", self._payload(hora="23:30"))
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hora", respuesta.data)

    def test_rechaza_numero_de_personas_sobre_la_capacidad(self):
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.post("/api/reservas/", self._payload(numero_personas=41))
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("numero_personas", respuesta.data)

    def test_rechaza_mas_de_veinte_personas_aunque_el_local_sea_grande(self):
        self.restaurante.capacidad = 100
        self.restaurante.save(update_fields=["capacidad"])
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.post("/api/reservas/", self._payload(numero_personas=25))
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("numero_personas", respuesta.data)


class ListarReservaTests(ReservaApiTestCase):
    def test_solo_devuelve_las_reservas_del_usuario_autenticado(self):
        Reserva.objects.create(
            usuario=self.usuario, restaurante=self.restaurante, fecha=self.manana, hora="20:00"
        )
        Reserva.objects.create(
            usuario=self.otro_usuario,
            restaurante=self.restaurante,
            fecha=self.manana,
            hora="20:00",
        )
        self.client.force_authenticate(self.usuario)
        respuesta = self.client.get("/api/reservas/")
        self.assertEqual(respuesta.data["count"], 1)


class CancelarReservaTests(ReservaApiTestCase):
    def setUp(self):
        super().setUp()
        self.reserva = Reserva.objects.create(
            usuario=self.usuario,
            restaurante=self.restaurante,
            fecha=self.manana,
            hora="20:00",
            estado=Reserva.Estado.CONFIRMADA,
        )
        self.client.force_authenticate(self.usuario)

    def test_cancela_una_reserva_pendiente_o_confirmada(self):
        respuesta = self.client.patch(f"/api/reservas/{self.reserva.id}/cancelar/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, Reserva.Estado.CANCELADA)

    def test_no_permite_cancelar_dos_veces(self):
        self.client.patch(f"/api/reservas/{self.reserva.id}/cancelar/")
        respuesta = self.client.patch(f"/api/reservas/{self.reserva.id}/cancelar/")
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permite_cancelar_una_reserva_completada(self):
        self.reserva.estado = Reserva.Estado.COMPLETADA
        self.reserva.save(update_fields=["estado"])
        respuesta = self.client.patch(f"/api/reservas/{self.reserva.id}/cancelar/")
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permite_cancelar_reserva_de_otro_usuario(self):
        self.client.force_authenticate(self.otro_usuario)
        respuesta = self.client.patch(f"/api/reservas/{self.reserva.id}/cancelar/")
        self.assertEqual(respuesta.status_code, status.HTTP_404_NOT_FOUND)
