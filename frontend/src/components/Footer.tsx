import Link from "next/link";

import { Logo } from "@/components/Logo";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border-subtle)] bg-[var(--surface)]">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-10 text-sm text-[var(--foreground)]/60 sm:px-6">
        <div className="flex items-center gap-2 font-display text-base text-[var(--foreground)]">
          <Logo className="h-7 w-7" />
          ReservaYa
        </div>
        <p>
          Un producto de{" "}
          <Link href="/nosotros" className="font-medium text-brand-600 hover:underline">
            Apta
          </Link>
          , empresa paraguaya de tecnología. Reservá mesa en los mejores restaurantes de Asunción,
          Encarnación y Ciudad del Este.
        </p>
        <p className="text-xs text-[var(--foreground)]/45">
          Los restaurantes listados son locales reales de Paraguay. Los horarios, cupos,
          teléfonos y estados de reserva que se muestran en esta versión son simulados con fines
          de demostración y no reflejan disponibilidad real ni están afiliados a esta plataforma.
        </p>
        <p>&copy; {new Date().getFullYear()} Apta. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
}
