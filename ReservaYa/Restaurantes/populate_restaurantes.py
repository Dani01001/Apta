# ReservaYa/Restaurantes/populate_restaurantes.py
"""
Script para poblar la base de datos con datos de ejemplo para Restaurantes y Mesas.
Este script es útil para desarrollo y pruebas.
Debe ejecutarse desde el directorio raíz del proyecto (donde está manage.py).
"""

import os
import sys
import django

# --- Configuración para ejecutar el script standalone ---
# Estas líneas son necesarias para que Django sepa cómo acceder a los modelos
# cuando se ejecuta este archivo directamente como un script.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReservaYa.settings') # Ajusta 'ReservaYa' al nombre real de tu proyecto
django.setup()
# --- Fin de configuración ---

# Importar modelos desde la app correcta
# Asegúrate de que estas rutas sean correctas
from Restaurantes.models import Restaurante, Mesa

# ... (imports y configuración iniciales) ...

def populate():
    """
    Función principal para poblar la base de datos.
    """
    print("=" * 50)
    print("Iniciando población de datos de ejemplo...")
    print("=" * 50)

    # --- Lista de restaurantes de ejemplo ---
    restaurantes_data = [
        {
            "nombre": "Lo de Osvaldo",
            "direccion": "Constitución 777 esq. Pettirossi, Asunción",
            "telefono": "0981 123456",
            "descripcion": "El tipo de cocina, sigue la técnica ancestral del uso de diferentes tipos de leña, el fuego y la brasa.",
            # === AGREGAR HORARIOS ===
            "horario_apertura": "08:00",  # Formato HH:MM
            "horario_cierre": "22:00",    # Formato HH:MM
        },
        {
            "nombre": "Bar San Roque",
            "direccion": "Av. Eusebio Ayala 1234, Asunción",
            "telefono": "0981 654321",
            "descripcion": "Bar tradicional con ambiente acogedor y buena música en vivo los fines de semana.",
            # === AGREGAR HORARIOS ===
            "horario_apertura": "18:00",
            "horario_cierre": "02:00", # Puede ser al día siguiente
        },
        {
            "nombre": "San Miguel",
            "direccion": "Mariscal López 567, Asunción",
            "telefono": "0981 112233",
            "descripcion": "Restaurante familiar con menú variado y precios accesibles.",
            # === AGREGAR HORARIOS ===
            "horario_apertura": "11:00",
            "horario_cierre": "23:00",
        },
        {
            "nombre": "Alma Cocina con Fuego",
            "direccion": "Avenida Republica Argentina 890, Asunción",
            "telefono": "0981 445566",
            "descripcion": "Cocina contemporánea con énfasis en productos locales y técnicas innovadoras.",
            # === AGREGAR HORARIOS ===
            "horario_apertura": "12:00",
            "horario_cierre": "22:30",
        },
        {
            "nombre": "Tierra Colorada",
            "direccion": "Ruta 1 km 20, San Lorenzo",
            "telefono": "0981 778899",
            "descripcion": "Restaurante campestre con especialidad en carnes a la parrilla y ambiente familiar.",
            # === AGREGAR HORARIOS ===
            "horario_apertura": "10:00",
            "horario_cierre": "21:00",
        }
    ]

    # --- Crear restaurantes ---
    restaurantes_creados = []
    print("--- Creando/Verificando Restaurantes ---")
    for i, data in enumerate(restaurantes_data, 1):
        try:
            # Extraer horarios del diccionario de datos
            horario_apertura = data.pop("horario_apertura") # pop lo saca del dict 'data'
            horario_cierre = data.pop("horario_cierre")     # pop lo saca del dict 'data'
            
            restaurante, created = Restaurante.objects.get_or_create(
                nombre=data["nombre"],
                defaults={
                    **data, # Incluye direccion, telefono, descripcion
                    "horario_apertura": horario_apertura,
                    "horario_cierre": horario_cierre,
                }
            )
            if created:
                print(f"  ✅ [{i}] Restaurante '{restaurante.nombre}' creado.")
            else:
                print(f"  ℹ️  [{i}] Restaurante '{restaurante.nombre}' ya existía.")
            restaurantes_creados.append(restaurante)
        except Exception as e:
            print(f"  ❌ Error al crear/obtener restaurante '{data['nombre']}': {e}")
            continue # Saltar a la siguiente iteración del loop

    if not restaurantes_creados:
        print("  ⚠️  No se crearon restaurantes. Verifica si hay errores.")
        return

    # --- Crear mesas para cada restaurante ---
    print("\n--- Creando/Verificando Mesas ---")
    total_mesas_creadas = 0
    for restaurante in restaurantes_creados:
        print(f"  Mesas para {restaurante.nombre}:")
        # Crear 5 mesas por restaurante
        for j in range(1, 6):
            numero_mesa = j
            # Capacidades variadas: 2, 4, 6, 8, 10
            capacidad_mesa = 2 * j 
            ubicacion_mesa = "Salón principal" if j <= 3 else "Terraza"
            
            try:
                mesa, created = Mesa.objects.get_or_create(
                    restaurante=restaurante,
                    numero=numero_mesa,
                    defaults={
                        "capacidad": capacidad_mesa,
                        "ubicacion": ubicacion_mesa
                    }
                )
                if created:
                    print(f"    ✅ Mesa {mesa.numero} (Capacidad: {mesa.capacidad}, Ubicación: {mesa.ubicacion}) creada.")
                    total_mesas_creadas += 1
                else:
                    print(f"    ℹ️  Mesa {mesa.numero} ya existía en {restaurante.nombre}.")
            except Exception as e:
                print(f"    ❌ Error al crear/obtener mesa {numero_mesa} para {restaurante.nombre}: {e}")

    print("\n" + "=" * 50)
    print(f"✅ Población de datos completada.")
    print(f"📊 Se procesaron {len(restaurantes_creados)} restaurantes.")
    print(f"📊 Se crearon/verificaron {total_mesas_creadas} mesas nuevas.")
    print("=" * 50)

# --- Punto de entrada del script ---
if __name__ == '__main__':
    # Si se ejecuta directamente desde la línea de comandos
    populate()
else:
    # Si se ejecuta con exec(open(...).read())
    print("🔍 Ejecutando populate() desde exec()...")
    populate()
    print("✅ Ejecución desde exec() finalizada.")
