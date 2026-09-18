import { FiltrosRestaurantes } from "@/components/FiltrosRestaurantes";
import { RestaurantCard } from "@/components/RestaurantCard";
import { apiFetch, buildQuery } from "@/lib/api";
import { CIUDADES } from "@/lib/categorias";
import type { Paginado, Restaurante } from "@/types";

interface PageProps {
  searchParams: Promise<Record<string, string | undefined>>;
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
  const data = await buscarRestaurantes({
    categoria: params.categoria,
    ciudad: params.ciudad,
    rango_precio: params.rango_precio,
    search: params.search,
  });

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
          </>
        )}
      </div>
    </div>
  );
}
