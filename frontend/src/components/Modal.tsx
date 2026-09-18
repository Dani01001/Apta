"use client";

import { X } from "lucide-react";
import { useEffect } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  abierto: boolean;
  onCerrar: () => void;
  titulo?: string;
  children: React.ReactNode;
  ancho?: "sm" | "md" | "lg";
}

const ANCHOS: Record<NonNullable<ModalProps["ancho"]>, string> = {
  sm: "max-w-sm",
  md: "max-w-md",
  lg: "max-w-2xl",
};

export function Modal({ abierto, onCerrar, titulo, children, ancho = "md" }: ModalProps) {
  useEffect(() => {
    if (!abierto) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") onCerrar();
    }
    document.addEventListener("keydown", onKeyDown);
    const overflowPrevio = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = overflowPrevio;
    };
  }, [abierto, onCerrar]);

  if (!abierto) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <button
        type="button"
        aria-label="Cerrar"
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onCerrar}
      />
      <div
        role="dialog"
        aria-modal="true"
        className={`relative w-full ${ANCHOS[ancho]} rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-6 shadow-xl`}
      >
        <button
          type="button"
          onClick={onCerrar}
          aria-label="Cerrar"
          className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full text-[var(--foreground)]/50 transition-colors hover:bg-black/5 hover:text-[var(--foreground)]"
        >
          <X className="h-4 w-4" />
        </button>
        {titulo && <h2 className="mb-4 pr-8 font-display text-xl font-semibold">{titulo}</h2>}
        {children}
      </div>
    </div>,
    document.body
  );
}
