import type { Metadata } from "next";

import { FiltrosRestaurantes } from "@/components/FiltrosRestaurantes";
import { Pagination } from "@/components/Pagination";
import { RestaurantCard } from "@/components/RestaurantCard";
import { apiFetch, buildQuery } from "@/lib/api";
import { CIUDADES } from "@/lib/categorias";
import type { Paginado, Restaurante } from "@/types";

const PAGE_SIZE = 12;

interface PageProps {
  searchParams: Promise<Record<string, string | undefined>>;
}

function filtrosDeParams(params: Record<string, string | undefined>) {
  return {
    categoria: params.categoria,
    ciudad: params.ciudad,
    rango_precio: params.rango_precio,
    search: params.search,
    page: params.page,
  };
}

export async function generateMetadata({ searchParams }: PageProps): Promise<Metadata> {
  const params = await searchParams;
  const partes = [params.ciudad, params.categoria, params.search].filter(Boolean);
  const titulo = partes.length ? `Restaurantes · ${partes.join(" · ")}` : "Restaurantes";
  return {
    title: titulo,
    description:
      "Filtra por categoría, ciudad o rango de precio y encuentra el restaurante perfecto en Paraguay.",
  };
}

async function buscarRestaurantes(params: Record<string, string | undefined>) {
  const query = buildQuery(params);
  try {
    return await apiFetch<Paginado<Restaurante>>(`/restaurantes/${query}`, {
      cache: "no-store",
    });
  } catch {
    return null;
  }
}

export default async function RestaurantesPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const filtros = filtrosDeParams(params);
  const data = await buscarRestaurantes(filtros);
  const paginaActual = Math.max(1, Number(params.page) || 1);
  const totalPaginas = data ? Math.max(1, Math.ceil(data.count / PAGE_SIZE)) : 1;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="mb-2 font-display text-3xl font-semibold">Restaurantes</h1>
      <p className="mb-6 text-[var(--foreground)]/70">
        Filtra por categoría, ciudad o rango de precio para encontrar el lugar perfecto.
      </p>

      <FiltrosRestaurantes ciudades={CIUDADES} />

      <div className="mt-8">
        {data === null ? (
          <div className="rounded-2xl border border-dashed border-[var(--border-subtle)] p-10 text-center text-[var(--foreground)]/60">
            No se pudo conectar con la API. Verifica que el backend de Django esté corriendo en
            http://127.0.0.1:8000.
          </div>
        ) : data.results.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-[var(--border-subtle)] p-10 text-center text-[var(--foreground)]/60">
            No encontramos restaurantes con esos filtros. Prueba con otra búsqueda.
          </div>
        ) : (
          <>
            <p className="mb-4 text-sm text-[var(--foreground)]/60">
              {data.count} restaurante{data.count === 1 ? "" : "s"} encontrado
              {data.count === 1 ? "" : "s"}
            </p>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {data.results.map((restaurante) => (
                <RestaurantCard key={restaurante.id} restaurante={restaurante} />
              ))}
            </div>
            <Pagination paginaActual={paginaActual} totalPaginas={totalPaginas} params={filtros} />
          </>
        )}
      </div>
    </div>
  );
}
