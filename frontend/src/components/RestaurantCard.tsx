import { MapPin, Star } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

import { CategoriaIcono } from "@/components/CategoriaIcono";
import type { Restaurante } from "@/types";

export function RestaurantCard({ restaurante }: { restaurante: Restaurante }) {
  return (
    <Link
      href={`/restaurantes/${restaurante.slug}`}
      className="group flex flex-col overflow-hidden rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] shadow-sm transition-shadow hover:shadow-lg"
    >
      <div className="relative aspect-[4/3] w-full overflow-hidden bg-brand-100">
        <Image
          src={restaurante.imagen_url}
          alt={restaurante.nombre}
          fill
          sizes="(min-width: 1024px) 320px, (min-width: 640px) 45vw, 90vw"
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
        {restaurante.destacado && (
          <span className="absolute left-3 top-3 rounded-full bg-brand-500 px-3 py-1 text-xs font-semibold text-white shadow">
            Destacado
          </span>
        )}
        <span className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-black/60 px-2.5 py-1 text-xs font-semibold text-white">
          <Star className="h-3 w-3 fill-current" />
          {restaurante.calificacion}
        </span>
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-display text-lg font-semibold leading-tight">
            {restaurante.nombre}
          </h3>
          <span className="shrink-0 text-sm font-medium text-[var(--foreground)]/60">
            {restaurante.rango_precio}
          </span>
        </div>
        <p className="text-sm text-[var(--foreground)]/70 line-clamp-2">
          {restaurante.descripcion}
        </p>
        <div className="mt-auto flex items-center gap-3 pt-2 text-xs font-medium text-[var(--foreground)]/60">
          <span className="flex items-center gap-1 rounded-full bg-brand-50 px-2.5 py-1 text-brand-700">
            <CategoriaIcono categoria={restaurante.categoria} className="h-3.5 w-3.5" />
            {restaurante.categoria_display}
          </span>
          <span className="flex items-center gap-1">
            <MapPin className="h-3.5 w-3.5" />
            {restaurante.ciudad}
          </span>
        </div>
      </div>
    </Link>
  );
}
