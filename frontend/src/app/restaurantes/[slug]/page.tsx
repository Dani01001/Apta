import { Clock, MapPin, Phone, Star, Tag, Users } from "lucide-react";
import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";

import { CategoriaIcono } from "@/components/CategoriaIcono";
import { ReservationForm } from "@/components/ReservationForm";
import { ApiError, apiFetch } from "@/lib/api";
import type { Restaurante } from "@/types";

interface PageProps {
  params: Promise<{ slug: string }>;
}

async function obtenerRestaurante(slug: string): Promise<Restaurante | null> {
  try {
    return await apiFetch<Restaurante>(`/restaurantes/${slug}/`, { cache: "no-store" });
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const restaurante = await obtenerRestaurante(slug);

  if (!restaurante) {
    return { title: "Restaurante no encontrado" };
  }

  const descripcion = `${restaurante.descripcion} Reservá mesa en ${restaurante.nombre}, ${restaurante.ciudad}.`;

  return {
    title: `${restaurante.nombre} — ${restaurante.ciudad}`,
    description: descripcion,
    openGraph: {
      title: `${restaurante.nombre} · ReservaYa`,
      description: descripcion,
      images: [{ url: restaurante.imagen_url }],
    },
    twitter: {
      card: "summary_large_image",
      images: [restaurante.imagen_url],
    },
  };
}

export default async function RestauranteDetallePage({ params }: PageProps) {
  const { slug } = await params;
  const restaurante = await obtenerRestaurante(slug);

  if (!restaurante) notFound();

  const info = [
    {
      icono: MapPin,
      etiqueta: "Ubicación",
      valor: `${restaurante.direccion}, ${restaurante.ciudad}`,
    },
    {
      icono: Clock,
      etiqueta: "Horario",
      valor: `${restaurante.hora_apertura.slice(0, 5)} a ${restaurante.hora_cierre.slice(0, 5)}`,
    },
    { icono: Phone, etiqueta: "Teléfono", valor: restaurante.telefono },
    { icono: Users, etiqueta: "Capacidad", valor: `${restaurante.capacidad} personas` },
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div className="grid gap-8 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <div className="relative mb-6 aspect-video w-full overflow-hidden rounded-2xl bg-brand-100">
            <Image
              src={restaurante.imagen_url}
              alt={restaurante.nombre}
              fill
              sizes="(min-width: 1024px) 60vw, 100vw"
              className="object-cover"
              priority
            />
          </div>

          <div className="mb-4 flex flex-wrap items-center gap-3">
            <span className="flex items-center gap-1.5 rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
              <CategoriaIcono categoria={restaurante.categoria} className="h-4 w-4" />
              {restaurante.categoria_display}
            </span>
            <span className="flex items-center gap-1 text-sm font-medium text-[var(--foreground)]/60">
              <Tag className="h-4 w-4" />
              {restaurante.rango_precio_display} ({restaurante.rango_precio})
            </span>
            <span className="flex items-center gap-1 text-sm font-medium text-[var(--foreground)]/60">
              <Star className="h-4 w-4 fill-brand-500 text-brand-500" />
              {restaurante.calificacion}
            </span>
          </div>

          <h1 className="mb-3 font-display text-3xl font-semibold sm:text-4xl">
            {restaurante.nombre}
          </h1>
          <p className="mb-6 text-[var(--foreground)]/70">{restaurante.descripcion}</p>

          <dl className="grid grid-cols-1 gap-5 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-5 sm:grid-cols-2">
            {info.map((item) => (
              <div key={item.etiqueta} className="flex items-start gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-brand-50 text-brand-600">
                  <item.icono className="h-4 w-4" />
                </span>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-[var(--foreground)]/50">
                    {item.etiqueta}
                  </dt>
                  <dd className="text-sm font-medium">{item.valor}</dd>
                </div>
              </div>
            ))}
          </dl>
        </div>

        <div className="lg:sticky lg:top-24 lg:self-start">
          <ReservationForm
            restauranteId={restaurante.id}
            restauranteNombre={restaurante.nombre}
            capacidad={restaurante.capacidad}
            horaApertura={restaurante.hora_apertura}
            horaCierre={restaurante.hora_cierre}
          />
        </div>
      </div>
    </div>
  );
}
