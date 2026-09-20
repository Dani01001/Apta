import { Compass } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Página no encontrada",
};

export default function NotFound() {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-4 px-4 py-24 text-center sm:px-6">
      <span className="flex h-16 w-16 items-center justify-center rounded-full bg-brand-50 text-brand-600">
        <Compass className="h-8 w-8" />
      </span>
      <h1 className="font-display text-3xl font-semibold text-ink-900">
        No encontramos esta página
      </h1>
      <p className="text-[var(--foreground)]/70">
        El enlace puede estar roto o el restaurante que buscas ya no está disponible. Volvé al
        inicio para seguir explorando.
      </p>
      <Link
        href="/"
        className="mt-2 rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-brand-600"
      >
        Volver al inicio
      </Link>
    </div>
  );
}
