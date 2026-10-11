"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
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
  fetchAutenticado: <T>(path: string, options?: RequestInit) => Promise<T>;
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
  const accessRef = useRef<string | null>(null);
  const refreshRef = useRef<string | null>(null);
  const renovando = useRef<Promise<string | null> | null>(null);

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
        accessRef.current = datos.access;
        refreshRef.current = datos.refresh;
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
    accessRef.current = datos.access;
    refreshRef.current = datos.refresh;
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
    accessRef.current = null;
    refreshRef.current = null;
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch {
      // nada que limpiar si localStorage no está disponible
    }
  }, []);


  const renovarAccess = useCallback(async (): Promise<string | null> => {
    const refresh = refreshRef.current;
    if (!refresh) return null;
    try {
      const datos = await apiFetch<{ access: string; refresh?: string }>("/usuarios/token/refresh/", {
        method: "POST",
        body: JSON.stringify({ refresh }),
      });
      accessRef.current = datos.access;
      if (datos.refresh) refreshRef.current = datos.refresh;
      setAccess(datos.access);
      try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const guardado: Almacenado = JSON.parse(raw);
          window.localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
              ...guardado,
              access: datos.access,
              refresh: refreshRef.current ?? guardado.refresh,
            } satisfies Almacenado)
          );
        }
      } catch {
        // Si no se puede guardar, la sesión renovada sigue en memoria
      }
      return datos.access;
    } catch {
      return null;
    }
  }, []);

  const fetchAutenticado = useCallback(
    async <T,>(path: string, options: RequestInit = {}): Promise<T> => {
      try {
        return await apiFetch<T>(path, { ...options, token: accessRef.current });
      } catch (err) {
        if (!(err instanceof ApiError) || err.status !== 401) throw err;
        // Varias llamadas que vencen juntas comparten una sola renovación
        renovando.current ??= renovarAccess().finally(() => {
          renovando.current = null;
        });
        const nuevo = await renovando.current;
        if (!nuevo) throw err;
        return apiFetch<T>(path, { ...options, token: nuevo });
      }
    },
    [renovarAccess]
  );

  const value = useMemo(
    () => ({ usuario, access, cargando, login, registrar, logout, fetchAutenticado }),
    [usuario, access, cargando, login, registrar, logout, fetchAutenticado]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return ctx;
}

export { ApiError };
