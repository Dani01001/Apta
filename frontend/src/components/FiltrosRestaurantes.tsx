"use client";

import { Search } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

import { CATEGORIAS, RANGOS_PRECIO } from "@/lib/categorias";

export function FiltrosRestaurantes({ ciudades }: { ciudades: string[] }) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [busqueda, setBusqueda] = useState(searchParams.get("search") ?? "");

  function actualizarFiltro(clave: string, valor: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (valor) {
      params.set(clave, valor);
    } else {
      params.delete(clave);
    }
    // Cualquier cambio de filtro vuelve a la primera página: los resultados
    // cambian, así que la página en la que estabas ya no tiene sentido.
    params.delete("page");
    router.push(`/restaurantes?${params.toString()}`);
  }

  return (
    <div className="grid gap-3 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-4 sm:grid-cols-2 lg:grid-cols-4">
      <form
        className="relative lg:col-span-1"
        onSubmit={(e) => {
          e.preventDefault();
          actualizarFiltro("search", busqueda);
        }}
      >
        <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--foreground)]/40" />
        <input
          type="search"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          placeholder="Buscar restaurante..."
          className="w-full rounded-full border border-[var(--border-subtle)] bg-transparent py-2 pl-10 pr-4 text-sm outline-none focus:border-brand-400"
        />
      </form>

      <select
        value={searchParams.get("categoria") ?? ""}
        onChange={(e) => actualizarFiltro("categoria", e.target.value)}
        className="rounded-full border border-[var(--border-subtle)] bg-transparent px-4 py-2 text-sm outline-none focus:border-brand-400"
      >
        <option value="">Todas las categorías</option>
        {CATEGORIAS.map((c) => (
          <option key={c.valor} value={c.valor}>
            {c.etiqueta}
          </option>
        ))}
      </select>

      <select
        value={searchParams.get("ciudad") ?? ""}
        onChange={(e) => actualizarFiltro("ciudad", e.target.value)}
        className="rounded-full border border-[var(--border-subtle)] bg-transparent px-4 py-2 text-sm outline-none focus:border-brand-400"
      >
        <option value="">Todas las ciudades</option>
        {ciudades.map((ciudad) => (
          <option key={ciudad} value={ciudad}>
            {ciudad}
          </option>
        ))}
      </select>

      <select
        value={searchParams.get("rango_precio") ?? ""}
        onChange={(e) => actualizarFiltro("rango_precio", e.target.value)}
        className="rounded-full border border-[var(--border-subtle)] bg-transparent px-4 py-2 text-sm outline-none focus:border-brand-400"
      >
        <option value="">Cualquier precio</option>
        {RANGOS_PRECIO.map((p) => (
          <option key={p.valor} value={p.valor}>
            {p.etiqueta}
          </option>
        ))}
      </select>
    </div>
  );
}
