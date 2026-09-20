"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { apiFetch, ApiError } from "@/lib/api";
import type { RespuestaAuth, Usuario } from "@/types";

interface RegistroInput {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  telefono?: string;
}

interface AuthContextValue {
  usuario: Usuario | null;
  access: string | null;
  cargando: boolean;
  login: (username: string, password: string) => Promise<void>;
  registrar: (datos: RegistroInput) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_KEY = "reservaya.auth";

interface Almacenado {
  access: string;
  refresh: string;
  usuario: Usuario;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [access, setAccess] = useState<string | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const datos: Almacenado = JSON.parse(raw);
        // Hidratación única de la sesión guardada en localStorage al montar: no hay
        // "external system" al que suscribirse, es una lectura de una sola vez.
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setUsuario(datos.usuario);
        setAccess(datos.access);
      }
    } catch {
      // localStorage no disponible o corrupto: se ignora y se inicia sin sesión
    } finally {
      setCargando(false);
    }
  }, []);

  const guardarSesion = useCallback((datos: RespuestaAuth) => {
    setUsuario(datos.usuario);
    setAccess(datos.access);
    try {
      window.localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          access: datos.access,
          refresh: datos.refresh,
          usuario: datos.usuario,
        } satisfies Almacenado)
      );
    } catch {
      // Guardado best-effort; la sesión sigue viva en memoria aunque falle
    }
  }, []);

  const login = useCallback(
    async (username: string, password: string) => {
      const datos = await apiFetch<RespuestaAuth>("/usuarios/login/", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      guardarSesion(datos);
    },
    [guardarSesion]
  );

  const registrar = useCallback(
    async (input: RegistroInput) => {
      const datos = await apiFetch<RespuestaAuth>("/usuarios/registro/", {
        method: "POST",
        body: JSON.stringify(input),
      });
      guardarSesion(datos);
    },
    [guardarSesion]
  );

  const logout = useCallback(() => {
    setUsuario(null);
    setAccess(null);
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch {
      // nada que limpiar si localStorage no está disponible
    }
  }, []);

  const value = useMemo(
    () => ({ usuario, access, cargando, login, registrar, logout }),
    [usuario, access, cargando, login, registrar, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return ctx;
}

export { ApiError };
