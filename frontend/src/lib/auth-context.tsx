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

import { apiFetch, ApiError, AUTH_URL } from "@/lib/api";
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

// Clave de la versión anterior, que guardaba los tokens en localStorage; se borra al cargar
const STORAGE_KEY_ANTERIOR = "reservaya.auth";
// Marca sin datos sensibles: indica que hay una cookie de sesión que vale la pena renovar al
// cargar. Sin ella, una visita sin sesión no dispara un 401 en la consola.
const MARCA_SESION = "reservaya.sesion";

function marcarSesion(activa: boolean) {
  try {
    if (activa) window.localStorage.setItem(MARCA_SESION, "1");
    else window.localStorage.removeItem(MARCA_SESION);
  } catch {
    // localStorage no disponible: se renueva siempre al cargar
  }
}

function haySesionMarcada() {
  try {
    return window.localStorage.getItem(MARCA_SESION) === "1";
  } catch {
    return true;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [access, setAccess] = useState<string | null>(null);
  const [cargando, setCargando] = useState(true);
  // El token de acceso vive solo en memoria; el de refresco, en una cookie HttpOnly
  const accessRef = useRef<string | null>(null);
  const renovando = useRef<Promise<string | null> | null>(null);

  const guardarSesion = useCallback((datos: RespuestaAuth) => {
    setUsuario(datos.usuario);
    setAccess(datos.access);
    accessRef.current = datos.access;
    marcarSesion(true);
  }, []);

  const limpiarSesion = useCallback(() => {
    setUsuario(null);
    setAccess(null);
    accessRef.current = null;
    marcarSesion(false);
  }, []);

  const renovarAccess = useCallback(async (): Promise<string | null> => {
    try {
      const datos = await apiFetch<RespuestaAuth>("/usuarios/token/refresh/", {
        method: "POST",
        base: AUTH_URL,
      });
      guardarSesion(datos);
      return datos.access;
    } catch {
      marcarSesion(false);
      return null;
    }
  }, [guardarSesion]);

  const renovarUnaVez = useCallback(() => {
    // Varias llamadas que vencen juntas comparten una sola renovación
    renovando.current ??= renovarAccess().finally(() => {
      renovando.current = null;
    });
    return renovando.current;
  }, [renovarAccess]);

  useEffect(() => {
    try {
      window.localStorage.removeItem(STORAGE_KEY_ANTERIOR);
    } catch {
      // localStorage no disponible: no hay nada viejo que borrar
    }
    if (!haySesionMarcada()) {
      // Lectura única al montar: no hay sesión que recuperar
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setCargando(false);
      return;
    }
    // Recupera la sesión desde la cookie de refresco al cargar la página
    renovarUnaVez().finally(() => setCargando(false));
  }, [renovarUnaVez]);

  const login = useCallback(
    async (username: string, password: string) => {
      const datos = await apiFetch<RespuestaAuth>("/usuarios/login/", {
        method: "POST",
        base: AUTH_URL,
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
        base: AUTH_URL,
        body: JSON.stringify(input),
      });
      guardarSesion(datos);
    },
    [guardarSesion]
  );

  const logout = useCallback(() => {
    limpiarSesion();
    // Invalida el refresco en el servidor y borra la cookie; si falla, la cookie vence sola
    apiFetch<void>("/usuarios/logout/", { method: "POST", base: AUTH_URL }).catch(() => {});
  }, [limpiarSesion]);

  const fetchAutenticado = useCallback(
    async <T,>(path: string, options: RequestInit = {}): Promise<T> => {
      try {
        return await apiFetch<T>(path, { ...options, token: accessRef.current });
      } catch (err) {
        if (!(err instanceof ApiError) || err.status !== 401) throw err;
        const nuevo = await renovarUnaVez();
        if (!nuevo) throw err;
        return apiFetch<T>(path, { ...options, token: nuevo });
      }
    },
    [renovarUnaVez]
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
