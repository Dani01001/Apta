"use client";

import { CalendarCheck, LogOut, Menu, X } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { Logo } from "@/components/Logo";
import { useAuth } from "@/lib/auth-context";
import { useAuthModal } from "@/lib/auth-modal-context";

const enlaces = [
  { href: "/", label: "Inicio" },
  { href: "/restaurantes", label: "Restaurantes" },
  { href: "/nosotros", label: "Nosotros" },
];

export function Navbar() {
  const { usuario, logout, cargando } = useAuth();
  const { abrirLogin, abrirRegistro } = useAuthModal();
  const pathname = usePathname();
  const router = useRouter();
  const [menuAbierto, setMenuAbierto] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-[var(--border-subtle)] bg-[var(--surface)]/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-2 font-display text-xl font-semibold text-brand-600">
          <Logo />
          ReservaYa
        </Link>

        <nav className="hidden items-center gap-6 text-sm font-medium sm:flex">
          {enlaces.map((enlace) => (
            <Link
              key={enlace.href}
              href={enlace.href}
              className={`transition-colors hover:text-brand-600 ${
                pathname === enlace.href ? "text-brand-600" : "text-[var(--foreground)]/80"
              }`}
            >
              {enlace.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 sm:flex">
          {cargando ? null : usuario ? (
            <>
              <Link
                href="/mis-reservas"
                className="flex items-center gap-1.5 text-sm font-medium text-[var(--foreground)]/80 hover:text-brand-600"
              >
                <CalendarCheck className="h-4 w-4" />
                Mis reservas
              </Link>
              <span className="text-sm text-[var(--foreground)]/60">
                Hola, {usuario.first_name || usuario.username}
              </span>
              <button
                onClick={() => {
                  logout();
                  router.push("/");
                }}
                className="flex items-center gap-1.5 rounded-full border border-[var(--border-subtle)] px-4 py-1.5 text-sm font-medium transition-colors hover:border-brand-400 hover:text-brand-600"
              >
                <LogOut className="h-3.5 w-3.5" />
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <button
                onClick={abrirLogin}
                className="text-sm font-medium text-[var(--foreground)]/80 hover:text-brand-600"
              >
                Iniciar sesión
              </button>
              <button
                onClick={abrirRegistro}
                className="rounded-full bg-brand-500 px-4 py-1.5 text-sm font-medium text-white shadow-sm transition-colors hover:bg-brand-600"
              >
                Crear cuenta
              </button>
            </>
          )}
        </div>

        <button
          className="flex h-9 w-9 items-center justify-center rounded-full border border-[var(--border-subtle)] sm:hidden"
          onClick={() => setMenuAbierto((v) => !v)}
          aria-label="Abrir menú"
        >
          {menuAbierto ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </button>
      </div>

      {menuAbierto && (
        <div className="border-t border-[var(--border-subtle)] px-4 py-3 sm:hidden">
          <nav className="flex flex-col gap-3 text-sm font-medium">
            {enlaces.map((enlace) => (
              <Link key={enlace.href} href={enlace.href} onClick={() => setMenuAbierto(false)}>
                {enlace.label}
              </Link>
            ))}
            {usuario ? (
              <>
                <Link href="/mis-reservas" onClick={() => setMenuAbierto(false)}>
                  Mis reservas
                </Link>
                <button
                  className="text-left text-brand-600"
                  onClick={() => {
                    logout();
                    setMenuAbierto(false);
                    router.push("/");
                  }}
                >
                  Cerrar sesión
                </button>
              </>
            ) : (
              <>
                <button
                  className="text-left"
                  onClick={() => {
                    setMenuAbierto(false);
                    abrirLogin();
                  }}
                >
                  Iniciar sesión
                </button>
                <button
                  className="text-left text-brand-600"
                  onClick={() => {
                    setMenuAbierto(false);
                    abrirRegistro();
                  }}
                >
                  Crear cuenta
                </button>
              </>
            )}
          </nav>
        </div>
      )}
    </header>
  );
}
