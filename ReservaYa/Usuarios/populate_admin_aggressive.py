import os
import sys

# =========================
# Configuración de entorno
# =========================
PROYECTO_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if PROYECTO_ROOT not in sys.path:
    sys.path.insert(0, PROYECTO_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReservaYa.settings")
import django
django.setup()

from django.contrib.auth import get_user_model
from Restaurantes.models import Restaurante, RestauranteAdmin
from django.db import IntegrityError, transaction
from django.utils.text import slugify

User = get_user_model()

# =========================
# Funciones auxiliares
# =========================

def generar_username_base(nombre_restaurante):
    base = slugify(nombre_restaurante).replace('-', '_')
    if not base:
        base = "admin_rest"
    return base.lower()

def username_unico(base):
    """Genera username único si ya existe en DB."""
    candidate = base
    i = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}_{i}"
        i += 1
    return candidate

# =========================
# Función de actualización / creación
# =========================

def sync_admins_por_restaurante(default_password="admin1234"):
    restaurantes = Restaurante.objects.all()
    print(f"📌 Encontrados {restaurantes.count()} restaurantes.")

    for restaurante in restaurantes:
        base_username = f"admin_{restaurante.slug}"
        email_sugerido = f"{base_username}@reserva.com"

        # Verificar si ya existe un usuario admin para este restaurante
        existing_admin = RestauranteAdmin.objects.filter(restaurante=restaurante).first()

        try:
            with transaction.atomic():
                if existing_admin:
                    user = existing_admin.usuario
                    updated = False
                    # Revisar rol
                    if user.role != User.ROLE_RESTAURANT:
                        user.role = User.ROLE_RESTAURANT
                        updated = True
                    # Revisar email
                    if user.email != email_sugerido:
                        user.email = email_sugerido
                        updated = True
                    # Revisar flag
                    if not getattr(user, 'is_restaurant_admin', True):
                        setattr(user, 'is_restaurant_admin', True)
                        updated = True
                    if updated:
                        user.save()
                        print(f"♻️  Usuario existente actualizado: {user.username} para {restaurante.nombre}")
                    else:
                        print(f"✅ Usuario existente correcto: {user.username} para {restaurante.nombre}")
                else:
                    # Crear nuevo usuario admin
                    username = username_unico(base_username)
                    user = User.objects.create_user(
                        username=username,
                        email=email_sugerido,
                        password=default_password,
                        role=User.ROLE_RESTAURANT
                    )
                    setattr(user, 'is_restaurant_admin', True)
                    user.save()

                    # Crear registro RestauranteAdmin
                    RestauranteAdmin.objects.create(
                        usuario=user,
                        restaurante=restaurante,
                        email_contacto=email_sugerido
                    )
                    print(f"🆕 Nuevo admin creado: {username} para {restaurante.nombre}")

        except IntegrityError as e:
            print(f"❌ Error procesando {restaurante.nombre}: {str(e)}")

# =========================
# Función principal
# =========================
def main():
    print("=== POPULATE ADMIN AGGRESSIVE (SYNC) ===")
    print("Este script actualizará y/o creará admins sin eliminar datos históricos.")
    confirm = input("¿Desea continuar? Escriba 'SI' para confirmar: ").strip()
    if confirm != "SI":
        print("Operación cancelada por el operador.")
        return

    sync_admins_por_restaurante(default_password="admin1234")
    print("\n✅ Operación finalizada. Recuerde cambiar contraseñas por defecto inmediatamente en producción.")

if __name__ == "__main__":
    main()
