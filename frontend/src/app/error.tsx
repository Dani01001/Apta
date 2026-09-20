"use client";

import { RefreshCcw, TriangleAlert } from "lucide-react";
import { useEffect } from "react";

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-4 px-4 py-24 text-center sm:px-6">
      <span className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100 text-red-600">
        <TriangleAlert className="h-8 w-8" />
      </span>
      <h1 className="font-display text-3xl font-semibold text-ink-900">Algo salió mal</h1>
      <p className="text-[var(--foreground)]/70">
        Ocurrió un error inesperado al cargar esta página. Podés intentarlo de nuevo.
      </p>
      <button
        onClick={reset}
        className="mt-2 flex items-center gap-2 rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-brand-600"
      >
        <RefreshCcw className="h-4 w-4" />
        Reintentar
      </button>
    </div>
  );
}
