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

El frontend está pensado para desplegarse en **Vercel** (encaja de forma nativa). El backend
Django, al depender de una base de datos con estado, funciona mejor en un servicio como
**Render** o **Railway** (free tier) que en Vercel, cuyo runtime serverless no persiste bien
SQLite. Ver `backend/.env.example` para las variables de entorno que hay que configurar en
producción (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `DATABASE_URL`).
