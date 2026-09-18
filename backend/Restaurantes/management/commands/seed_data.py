import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from Reservas.models import Reserva
from Restaurantes.models import Restaurante
from Usuarios.models import Perfil

# Restaurantes reales de Paraguay (Asunción, Encarnación y Ciudad del Este).
# Los datos operativos (teléfono, horario, cupos, calificación) son simulados
# con fines de demostración y no reflejan disponibilidad real del local.
RESTAURANTES = [
    {
        "nombre": "La Cabrera Asunción",
        "categoria": "parrilla",
        "ciudad": "Asunción",
        "zona": "Villa Morra",
        "rango_precio": "$$$$",
        "calificacion": 4.8,
        "descripcion": "Sucursal asuncena de la icónica parrilla porteña, famosa por su ojo de bife y sus guarniciones de autor.",
        "destacado": True,
    },
    {
        "nombre": "Lo de Osvaldo",
        "categoria": "parrilla",
        "ciudad": "Asunción",
        "zona": "Carmelitas",
        "rango_precio": "$$$",
        "calificacion": 4.6,
        "descripcion": "Parrilla tradicional paraguaya con técnicas de alta cocina y una selección exigente de cortes.",
        "destacado": True,
    },
    {
        "nombre": "Churrasquería O Gaúcho",
        "categoria": "parrilla",
        "ciudad": "Asunción",
        "zona": "Villa Morra",
        "rango_precio": "$$$",
        "calificacion": 4.5,
        "descripcion": "Espacio de aire brasileño con rodizio de carnes y ambiente latino para compartir en grupo.",
        "destacado": False,
    },
    {
        "nombre": "El Bolsi",
        "categoria": "cafeteria",
        "ciudad": "Asunción",
        "zona": "Casco Histórico",
        "direccion": "Estrella 399 esq. Alberdi",
        "rango_precio": "$$",
        "calificacion": 4.7,
        "descripcion": "Confitería y restaurante fundado en 1960, patrimonio del centro de Asunción, con carta paraguaya, pastas y repostería.",
        "destacado": True,
    },
    {
        "nombre": "Tierra Colorada",
        "categoria": "paraguaya",
        "ciudad": "Asunción",
        "zona": "Carmelitas",
        "rango_precio": "$$$$",
        "calificacion": 4.9,
        "descripcion": "Cocina paraguaya de autor liderada por el chef Rodolfo Angenscheidt, con ingredientes autóctonos como la mandioca reinterpretados con técnica contemporánea.",
        "destacado": True,
    },
    {
        "nombre": "Casa Lorenzo",
        "categoria": "internacional",
        "ciudad": "Asunción",
        "zona": "Villa Morra",
        "rango_precio": "$$$$",
        "calificacion": 4.9,
        "descripcion": "Cocina europea contemporánea con producto de estación, ambiente elegante y una repostería reconocida por la crítica gastronómica local.",
        "destacado": True,
    },
    {
        "nombre": "Josephine de Talleyrand",
        "categoria": "internacional",
        "ciudad": "Asunción",
        "zona": "Recoleta",
        "rango_precio": "$$$",
        "calificacion": 4.6,
        "descripcion": "Parte del histórico Grupo Talleyrand, propone alta cocina internacional en un salón clásico y sobrio.",
        "destacado": False,
    },
    {
        "nombre": "Maurice",
        "categoria": "internacional",
        "ciudad": "Asunción",
        "zona": "Recoleta",
        "rango_precio": "$$$$",
        "calificacion": 4.7,
        "descripcion": "La faceta más formal del Grupo Talleyrand: alta cocina francesa con técnica depurada y servicio meticuloso.",
        "destacado": False,
    },
    {
        "nombre": "Pez de Mar Dulce",
        "categoria": "mariscos",
        "ciudad": "Asunción",
        "zona": "Villa Morra",
        "rango_precio": "$$$",
        "calificacion": 4.5,
        "descripcion": "Especialistas en pescados y frutos de río, con propuestas frescas centradas en el surubí y otras especies regionales.",
        "destacado": False,
    },
    {
        "nombre": "Combitos Restaurante Vegetariano",
        "categoria": "vegetariana",
        "ciudad": "Asunción",
        "zona": "Villa Morra",
        "rango_precio": "$$",
        "calificacion": 4.4,
        "descripcion": "Opciones vegetarianas y veganas caseras, con buenas porciones y personal atento a cada preferencia alimentaria.",
        "destacado": False,
    },
    {
        "nombre": "Parrilla Don Quincho",
        "categoria": "parrilla",
        "ciudad": "Encarnación",
        "zona": "Centro",
        "rango_precio": "$$$",
        "calificacion": 4.5,
        "descripcion": "Referente de carnes a la parrilla en Encarnación, con cortes de calidad y guarniciones tradicionales.",
        "destacado": False,
    },
    {
        "nombre": "Restaurante El Quincho",
        "categoria": "paraguaya",
        "ciudad": "Encarnación",
        "zona": "Centro",
        "rango_precio": "$$",
        "calificacion": 4.4,
        "descripcion": "Cocina paraguaya de siempre: asado a la parrilla, sopa paraguaya y chipa guazú en pleno centro de la ciudad.",
        "destacado": False,
    },
    {
        "nombre": "La Carreta",
        "categoria": "paraguaya",
        "ciudad": "Encarnación",
        "zona": "Costanera",
        "rango_precio": "$$",
        "calificacion": 4.3,
        "descripcion": "Platos típicos como surubí a la parrilla, vorí vorí de pollo y mbeju, en un ambiente familiar.",
        "destacado": False,
    },
    {
        "nombre": "Primoli Restaurante",
        "categoria": "internacional",
        "ciudad": "Encarnación",
        "zona": "Centro",
        "rango_precio": "$$$",
        "calificacion": 4.6,
        "descripcion": "Uno de los favoritos de Encarnación, con carta internacional, buen servicio y una propuesta cuidada de principio a fin.",
        "destacado": True,
    },
    {
        "nombre": "Bel Sit di Giorgio",
        "categoria": "italiana",
        "ciudad": "Ciudad del Este",
        "zona": "Centro",
        "rango_precio": "$$$",
        "calificacion": 4.5,
        "descripcion": "Cocina italiana tradicional muy reconocida en Ciudad del Este, con pastas caseras y clásicos de la trattoria.",
        "destacado": False,
    },
    {
        "nombre": "Origami Sushi Bar and Grill",
        "categoria": "japonesa",
        "ciudad": "Ciudad del Este",
        "zona": "Country Club",
        "rango_precio": "$$$",
        "calificacion": 4.5,
        "descripcion": "Barra de sushi y grill japonés con carta completa, cócteles y una ambientación cuidada dentro del Country Club.",
        "destacado": False,
    },
]

PREFIJO_TELEFONO = {
    "Asunción": "+595 21",
    "Encarnación": "+595 71",
    "Ciudad del Este": "+595 61",
}

USUARIOS = [
    {
        "username": "demo",
        "email": "demo@apta.com.py",
        "first_name": "Usuario",
        "last_name": "Demo",
        "password": "Demo1234",
        "telefono": "+595 981 111 222",
    },
    {
        "username": "maria.gonzalez",
        "email": "maria.gonzalez@example.com",
        "first_name": "María",
        "last_name": "González",
        "password": "Demo1234",
        "telefono": "+595 982 222 333",
    },
    {
        "username": "diego.benitez",
        "email": "diego.benitez@example.com",
        "first_name": "Diego",
        "last_name": "Benítez",
        "password": "Demo1234",
        "telefono": "+595 983 333 444",
    },
]


class Command(BaseCommand):
    help = "Carga restaurantes reales de Paraguay y datos simulados de usuarios y reservas para la demo de ReservaYa."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina los datos existentes antes de sembrar los nuevos.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Eliminando datos existentes...")
            Reserva.objects.all().delete()
            Restaurante.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        restaurantes = self._crear_restaurantes()
        usuarios = self._crear_usuarios()

        if options["reset"] or not Reserva.objects.exists():
            self._crear_reservas(usuarios, restaurantes)
        else:
            self.stdout.write(
                "Ya existen reservas: se omite la siembra de reservas para no pisar datos reales "
                "(usa --reset si querés forzarla)."
            )

        self.stdout.write(self.style.SUCCESS("Datos cargados correctamente."))
        self.stdout.write("Usuario demo -> username: demo / password: Demo1234")

    def _crear_restaurantes(self):
        creados = []
        for data in RESTAURANTES:
            slug = slugify(data["nombre"])
            prefijo = PREFIJO_TELEFONO[data["ciudad"]]
            direccion = data.get("direccion") or data["zona"]
            restaurante, _ = Restaurante.objects.update_or_create(
                slug=slug,
                defaults={
                    "nombre": data["nombre"],
                    "descripcion": data["descripcion"],
                    "categoria": data["categoria"],
                    "ciudad": data["ciudad"],
                    "direccion": direccion,
                    "telefono": f"{prefijo} {random.randint(200, 999)} {random.randint(100, 999)}",
                    "rango_precio": data["rango_precio"],
                    "calificacion": data["calificacion"],
                    "capacidad": random.choice([30, 40, 50, 60, 80]),
                    "imagen_url": f"https://picsum.photos/seed/{slug}/800/600",
                    "destacado": data["destacado"],
                    "activo": True,
                },
            )
            creados.append(restaurante)
        self.stdout.write(f"{len(creados)} restaurantes sembrados.")
        return creados

    def _crear_usuarios(self):
        creados = []
        for data in USUARIOS:
            usuario, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                },
            )
            if created:
                usuario.set_password(data["password"])
                usuario.save()
            Perfil.objects.update_or_create(
                usuario=usuario, defaults={"telefono": data["telefono"]}
            )
            creados.append(usuario)
        self.stdout.write(f"{len(creados)} usuarios sembrados.")
        return creados

    def _crear_reservas(self, usuarios, restaurantes):
        Reserva.objects.all().delete()
        hoy = timezone.localdate()
        estados = [
            Reserva.Estado.CONFIRMADA,
            Reserva.Estado.PENDIENTE,
            Reserva.Estado.COMPLETADA,
            Reserva.Estado.CANCELADA,
        ]
        horas = ["13:00", "13:30", "19:00", "19:30", "20:00", "20:30", "21:00"]
        total = 0
        for usuario in usuarios:
            for offset in [-14, -5, 3, 9, 20]:
                restaurante = random.choice(restaurantes)
                fecha = hoy + timedelta(days=offset)
                estado = (
                    Reserva.Estado.COMPLETADA
                    if offset < 0
                    else random.choice(estados[:2])
                )
                Reserva.objects.create(
                    usuario=usuario,
                    restaurante=restaurante,
                    fecha=fecha,
                    hora=random.choice(horas),
                    numero_personas=random.randint(2, 6),
                    estado=estado,
                    notas="Mesa junto a la ventana, por favor." if offset % 2 == 0 else "",
                )
                total += 1
        self.stdout.write(f"{total} reservas sembradas.")
