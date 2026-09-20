import { ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";

export function Pagination({
  paginaActual,
  totalPaginas,
  params,
}: {
  paginaActual: number;
  totalPaginas: number;
  params: Record<string, string | undefined>;
}) {
  if (totalPaginas <= 1) return null;

  function hrefPagina(pagina: number) {
    const busqueda = new URLSearchParams();
    Object.entries(params).forEach(([clave, valor]) => {
      if (valor && clave !== "page") busqueda.set(clave, valor);
    });
    if (pagina > 1) busqueda.set("page", String(pagina));
    const qs = busqueda.toString();
    return `/restaurantes${qs ? `?${qs}` : ""}`;
  }

  const anteriorDeshabilitado = paginaActual <= 1;
  const siguienteDeshabilitado = paginaActual >= totalPaginas;

  return (
    <nav
      aria-label="Paginación de restaurantes"
      className="mt-10 flex items-center justify-center gap-4"
    >
      <Link
        href={hrefPagina(paginaActual - 1)}
        aria-disabled={anteriorDeshabilitado}
        tabIndex={anteriorDeshabilitado ? -1 : undefined}
        className={`flex h-10 w-10 items-center justify-center rounded-full border border-[var(--border-subtle)] transition-colors ${
          anteriorDeshabilitado
            ? "pointer-events-none opacity-40"
            : "hover:border-brand-400 hover:text-brand-600"
        }`}
      >
        <ChevronLeft className="h-4 w-4" />
      </Link>
      <span className="text-sm font-medium text-[var(--foreground)]/70">
        Página {paginaActual} de {totalPaginas}
      </span>
      <Link
        href={hrefPagina(paginaActual + 1)}
        aria-disabled={siguienteDeshabilitado}
        tabIndex={siguienteDeshabilitado ? -1 : undefined}
        className={`flex h-10 w-10 items-center justify-center rounded-full border border-[var(--border-subtle)] transition-colors ${
          siguienteDeshabilitado
            ? "pointer-events-none opacity-40"
            : "hover:border-brand-400 hover:text-brand-600"
        }`}
      >
        <ChevronRight className="h-4 w-4" />
      </Link>
    </nav>
  );
}
