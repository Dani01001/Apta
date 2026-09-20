import { Code2, Handshake, Mail, MapPin, Sparkles, Target } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Nosotros",
  description:
    "Conocé Apta, la empresa paraguaya de tecnología detrás de ReservaYa: nuestra misión, visión, valores y el equipo fundador.",
};

const EQUIPO = [
  {
    nombre: "Jesús Amarilla",
    cargo: "Cofundador y Desarrollador Full-Stack",
    bio: "Lidera la arquitectura técnica de ReservaYa, desde la API hasta la experiencia de reserva en el navegador.",
  },
  {
    nombre: "Rodrigo Aveiro",
    cargo: "Cofundador y Desarrollador Full-Stack",
    bio: "Impulsa la calidad del producto en cada entrega, cuidando el detalle en el código y en la experiencia final.",
  },
  {
    nombre: "Toshi Pedrozo",
    cargo: "Cofundador y Desarrollador Full-Stack",
    bio: "Construye la base técnica que permite a ReservaYa crecer a nuevas ciudades y restaurantes de forma sólida.",
  },
];

const VALORES = [
  {
    icono: Target,
    titulo: "Cercanía",
    descripcion: "Diseñamos cada funcionalidad pensando en cómo reservan realmente los paraguayos.",
  },
  {
    icono: Sparkles,
    titulo: "Simplicidad",
    descripcion: "Reservar una mesa debería tomar segundos, no llamadas ni esperas innecesarias.",
  },
  {
    icono: Handshake,
    titulo: "Confianza",
    descripcion: "Trabajamos junto a los restaurantes para que cada reserva sea clara para ambas partes.",
  },
];

function iniciales(nombre: string) {
  return nombre
    .split(" ")
    .map((parte) => parte[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

export default function NosotrosPage() {
  return (
    <div>
      <section className="bg-gradient-to-br from-brand-50 via-cream-50 to-cream-100">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:px-6">
          <span className="mb-4 inline-block rounded-full bg-brand-100 px-4 py-1 text-sm font-medium text-brand-700">
            Somos Apta
          </span>
          <h1 className="mb-4 font-display text-4xl font-semibold text-ink-900 sm:text-5xl">
            Hacemos que reservar una mesa sea así de fácil
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-[var(--foreground)]/70">
            Apta es una empresa paraguaya de tecnología. Creamos ReservaYa para conectar a las
            personas con los restaurantes que aman, sin llamadas, sin esperas y sin fricción.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
        <div className="grid gap-10 sm:grid-cols-2">
          <div>
            <h2 className="mb-3 font-display text-2xl font-semibold">Nuestra misión</h2>
            <p className="text-[var(--foreground)]/70">
              Acercar la mejor gastronomía de Paraguay a cualquier persona con un celular en la
              mano. Creemos que encontrar mesa en tu restaurante favorito no debería ser
              complicado, y trabajamos para que cada reserva sea simple, rápida y confiable.
            </p>
          </div>
          <div>
            <h2 className="mb-3 font-display text-2xl font-semibold">Nuestra visión</h2>
            <p className="text-[var(--foreground)]/70">
              Ser la plataforma de reservas de referencia en Paraguay, presente en Asunción,
              Encarnación, Ciudad del Este y cada ciudad donde haya un buen restaurante esperando
              a sus próximos comensales.
            </p>
          </div>
        </div>
      </section>

      <section className="bg-[var(--surface)] py-16">
        <div className="mx-auto max-w-5xl px-4 sm:px-6">
          <h2 className="mb-8 text-center font-display text-2xl font-semibold">
            Lo que nos guía
          </h2>
          <div className="grid gap-6 sm:grid-cols-3">
            {VALORES.map((valor) => (
              <div
                key={valor.titulo}
                className="rounded-2xl border border-[var(--border-subtle)] p-6 text-center"
              >
                <span className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-brand-50 text-brand-600">
                  <valor.icono className="h-5 w-5" />
                </span>
                <h3 className="mb-1 font-display text-lg font-semibold">{valor.titulo}</h3>
                <p className="text-sm text-[var(--foreground)]/70">{valor.descripcion}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
        <h2 className="mb-2 text-center font-display text-2xl font-semibold">
          El equipo detrás de Apta
        </h2>
        <p className="mb-10 text-center text-[var(--foreground)]/70">
          Tres cofundadores construyendo ReservaYa de punta a punta.
        </p>
        <div className="grid gap-6 sm:grid-cols-3">
          {EQUIPO.map((persona) => (
            <div
              key={persona.nombre}
              className="flex flex-col items-center rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-6 text-center"
            >
              <span className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-brand-500 font-display text-xl font-semibold text-white">
                {iniciales(persona.nombre)}
              </span>
              <h3 className="font-display text-lg font-semibold">{persona.nombre}</h3>
              <p className="mb-2 flex items-center gap-1.5 text-sm font-medium text-brand-600">
                <Code2 className="h-3.5 w-3.5" />
                {persona.cargo}
              </p>
              <p className="text-sm text-[var(--foreground)]/70">{persona.bio}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-[var(--surface)] py-16">
        <div className="mx-auto flex max-w-3xl flex-col items-center gap-4 px-4 text-center sm:px-6">
          <h2 className="font-display text-2xl font-semibold">Hablemos</h2>
          <p className="text-[var(--foreground)]/70">
            ¿Tenés un restaurante y querés sumarte a ReservaYa? Escribinos.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <a
              href="mailto:hola@apta.com.py"
              className="flex items-center justify-center gap-2 rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-brand-600"
            >
              <Mail className="h-4 w-4" />
              hola@apta.com.py
            </a>
            <span className="flex items-center justify-center gap-2 rounded-full border border-[var(--border-subtle)] px-6 py-2.5 text-sm font-medium text-[var(--foreground)]/70">
              <MapPin className="h-4 w-4" />
              Asunción, Paraguay
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
