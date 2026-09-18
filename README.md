# ReservaYa

Plataforma de reservas de restaurantes de Paraguay, un producto de **Apta**. Backend API en
**Django REST Framework** y frontend en **Next.js (TypeScript + Tailwind CSS)**.

Los restaurantes listados (Asunción, Encarnación y Ciudad del Este) son **locales reales de
Paraguay**. Los datos operativos —horarios, teléfonos, cupos y estados de reserva— se generan con
un comando de seed y son simulados con fines de demostración; no reflejan disponibilidad real ni
implican afiliación con esta plataforma.

## Estructura del repositorio

```
Apta/
├── backend/          # API REST con Django + DRF (apps: Usuarios, Restaurantes, Reservas)
└── frontend/          # Aplicación Next.js (App Router) que consume la API
```

## Backend (Django REST Framework)

Requiere Python 3.10+.

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
copy .env.example .env       # Windows (o cp en macOS/Linux)

python manage.py migrate
python manage.py seed_data   # carga restaurantes reales de Paraguay + usuarios y reservas simulados
python manage.py createsuperuser   # opcional, para entrar a /admin/

python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

### Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/usuarios/registro/` | Crea una cuenta y devuelve tokens JWT |
| POST | `/api/usuarios/login/` | Login, devuelve `access`/`refresh` y datos del usuario |
| GET/PATCH | `/api/usuarios/me/` | Perfil del usuario autenticado |
| GET | `/api/restaurantes/` | Lista restaurantes (filtros: `categoria`, `ciudad`, `rango_precio`, `search`) |
| GET | `/api/restaurantes/<slug>/` | Detalle de un restaurante |
| GET/POST | `/api/reservas/` | Lista o crea reservas del usuario autenticado |
| PATCH | `/api/reservas/<id>/cancelar/` | Cancela una reserva |

### Usuario demo (creado por `seed_data`)

- **Usuario:** `demo`
- **Contraseña:** `Demo1234`

## Frontend (Next.js)

Requiere Node.js 18+.

```bash
cd frontend
npm install
copy .env.local.example .env.local   # Windows (o cp en macOS/Linux)
npm run dev
```

La app queda disponible en `http://localhost:3000` y consume la API en la URL definida por
`NEXT_PUBLIC_API_URL` (por defecto `http://127.0.0.1:8000/api`).

### Páginas y modales

Páginas con URL propia (navegables y compartibles):

- `/` — landing con categorías y restaurantes destacados
- `/restaurantes` — listado con filtros (categoría, ciudad, precio, búsqueda)
- `/restaurantes/[slug]` — detalle del restaurante + formulario de reserva
- `/nosotros` — información de Apta, misión, valores y equipo fundador
- `/mis-reservas` — reservas del usuario autenticado

Flujos resueltos con **modal** en vez de página propia, por ser acciones puntuales que no
necesitan una URL dedicada:

- **Iniciar sesión / Crear cuenta** — un solo modal con pestañas, disponible desde cualquier
  página (navbar o al intentar reservar sin sesión).
- **Confirmación de reserva creada** — modal de éxito con acceso directo a "Mis reservas".
- **Confirmación de cancelación** — modal de confirmación antes de cancelar una reserva.

Todos los iconos son de [lucide-react](https://lucide.dev/) (sin emojis) para mantener una
estética minimalista y consistente.

## Despliegue

### Frontend — Vercel

Desplegado en `https://reservaya-umber.vercel.app`. El proyecto está conectado al repositorio
de GitHub, por lo que cada push a `main` genera un nuevo despliegue automáticamente.

### Backend — Render

El backend Django, al depender de una base de datos con estado, no encaja bien en el runtime
serverless de Vercel (no persiste SQLite entre invocaciones). Se despliega en **Render** usando
el archivo `render.yaml` de la raíz del repositorio (Blueprint):

1. Crear una cuenta en [render.com](https://render.com) (gratis, se puede usar GitHub para
   entrar).
2. En el dashboard: **New +** → **Blueprint** → seleccionar el repositorio `Dani01001/Apta`.
   Render detecta `render.yaml` y crea automáticamente el servicio web y la base de datos
   Postgres gratuita.
3. Una vez desplegado, abrir la pestaña **Shell** del servicio y correr una sola vez:
   `python manage.py seed_data` (carga los restaurantes reales y los datos de demo).
4. Copiar la URL pública que asigna Render (algo como `https://reservaya-api.onrender.com`) y
   actualizar la variable `NEXT_PUBLIC_API_URL` del proyecto en Vercel con
   `https://<esa-url>/api`, luego volver a desplegar el frontend.

Ver `backend/.env.example` para el resto de variables de entorno de producción
(`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `DATABASE_URL`), todas ya
precompletadas en `render.yaml`.
