import { MapPinned } from "lucide-react";
import Link from "next/link";

import { RestaurantCard } from "@/components/RestaurantCard";
import { apiFetch } from "@/lib/api";
import { CATEGORIAS } from "@/lib/categorias";
import type { Paginado, Restaurante } from "@/types";

async function obtenerDestacados(): Promise<Restaurante[]> {
  try {
    const data = await apiFetch<Paginado<Restaurante>>(
      "/restaurantes/?ordering=-calificacion",
      { cache: "no-store" }
    );
    return data.results.slice(0, 6);
  } catch {
    return [];
  }
}

export default async function HomePage() {
  const destacados = await obtenerDestacados();

  return (
    <div>
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-50 via-cream-50 to-cream-100">
        <div className="mx-auto flex max-w-6xl flex-col items-start gap-6 px-4 py-20 sm:px-6 lg:py-28">
          <span className="flex items-center gap-2 rounded-full bg-brand-100 px-4 py-1 text-sm font-medium text-brand-700">
            <MapPinned className="h-4 w-4" />
            Asunción · Encarnación · Ciudad del Este
          </span>
          <h1 className="max-w-2xl font-display text-4xl font-semibold leading-tight text-ink-900 sm:text-5xl lg:text-6xl">
            Reserva tu mesa favorita en segundos
          </h1>
          <p className="max-w-xl text-lg text-[var(--foreground)]/70">
            ReservaYa conecta a los amantes de la buena mesa con los mejores restaurantes de
            Paraguay. Explora, compara y reserva sin llamadas ni esperas.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/restaurantes"
              className="rounded-full bg-brand-500 px-6 py-3 text-sm font-semibold text-white shadow-md transition-colors hover:bg-brand-600"
            >
              Explorar restaurantes
            </Link>
            <Link
              href="/nosotros"
              className="rounded-full border border-brand-300 px-6 py-3 text-sm font-semibold text-brand-700 transition-colors hover:bg-brand-50"
            >
              Conocer Apta
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2 className="mb-6 font-display text-2xl font-semibold">Explora por categoría</h2>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {CATEGORIAS.map((cat) => {
            const Icono = cat.icono;
            return (
              <Link
                key={cat.valor}
                href={`/restaurantes?categoria=${cat.valor}`}
                className="flex flex-col items-center gap-2 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] px-4 py-6 text-center transition-shadow hover:shadow-md"
              >
                <span className="flex h-11 w-11 items-center justify-center rounded-full bg-brand-50 text-brand-600">
                  <Icono className="h-5 w-5" />
                </span>
                <span className="text-sm font-medium">{cat.etiqueta}</span>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-display text-2xl font-semibold">Restaurantes destacados</h2>
          <Link href="/restaurantes" className="text-sm font-medium text-brand-600 hover:underline">
            Ver todos
          </Link>
        </div>
        {destacados.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-[var(--border-subtle)] p-10 text-center text-[var(--foreground)]/60">
            No se pudo conectar con la API. Verifica que el backend de Django esté corriendo en
            http://127.0.0.1:8000.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {destacados.map((restaurante) => (
              <RestaurantCard key={restaurante.id} restaurante={restaurante} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
