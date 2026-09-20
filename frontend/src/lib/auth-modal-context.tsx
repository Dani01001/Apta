"use client";

import { createContext, useCallback, useContext, useMemo, useState } from "react";

import { AuthModal } from "@/components/AuthModal";

type VistaAuth = "login" | "registro";

interface AuthModalContextValue {
  abrirLogin: () => void;
  abrirRegistro: () => void;
  cerrar: () => void;
}

const AuthModalContext = createContext<AuthModalContextValue | undefined>(undefined);

export function AuthModalProvider({ children }: { children: React.ReactNode }) {
  const [vista, setVista] = useState<VistaAuth | null>(null);

  const abrirLogin = useCallback(() => setVista("login"), []);
  const abrirRegistro = useCallback(() => setVista("registro"), []);
  const cerrar = useCallback(() => setVista(null), []);

  const value = useMemo(() => ({ abrirLogin, abrirRegistro, cerrar }), [abrirLogin, abrirRegistro, cerrar]);

  return (
    <AuthModalContext.Provider value={value}>
      {children}
      <AuthModal vista={vista} onCambiarVista={setVista} onCerrar={cerrar} />
    </AuthModalContext.Provider>
  );
}

export function useAuthModal() {
  const ctx = useContext(AuthModalContext);
  if (!ctx) throw new Error("useAuthModal debe usarse dentro de AuthModalProvider");
  return ctx;
}
