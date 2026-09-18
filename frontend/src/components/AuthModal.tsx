"use client";

import { useState } from "react";

import { Modal } from "@/components/Modal";
import { ApiError, extraerMensajeError } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

type VistaAuth = "login" | "registro";

const estiloInput =
  "rounded-lg border border-[var(--border-subtle)] bg-transparent px-3 py-2 outline-none focus:border-brand-400";
const estiloLabel = "flex flex-col gap-1 text-sm";
const estiloBoton =
  "rounded-full bg-brand-500 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-brand-600 disabled:opacity-60";

function FormularioLogin({ onExito }: { onExito: () => void }) {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setCargando(true);
    try {
      await login(username, password);
      onExito();
    } catch (err) {
      const detail = err instanceof ApiError ? err.detail : undefined;
      setError(extraerMensajeError(detail, "Usuario o contraseña incorrectos."));
    } finally {
      setCargando(false);
    }
  }

  return (
    <form onSubmit={enviar} className="flex flex-col gap-4">
      <p className="text-sm text-[var(--foreground)]/70">
        Cuenta de prueba: <strong>demo</strong> / <strong>Demo1234</strong>
      </p>
      <label className={estiloLabel}>
        Usuario
        <input required value={username} onChange={(e) => setUsername(e.target.value)} className={estiloInput} />
      </label>
      <label className={estiloLabel}>
        Contraseña
        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={estiloInput}
        />
      </label>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button type="submit" disabled={cargando} className={estiloBoton}>
        {cargando ? "Ingresando..." : "Ingresar"}
      </button>
    </form>
  );
}

function FormularioRegistro({ onExito }: { onExito: () => void }) {
  const { registrar } = useAuth();
  const [form, setForm] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    telefono: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);

  function actualizar(campo: string, valor: string) {
    setForm((prev) => ({ ...prev, [campo]: valor }));
  }

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setCargando(true);
    try {
      await registrar(form);
      onExito();
    } catch (err) {
      const detail = err instanceof ApiError ? err.detail : undefined;
      setError(extraerMensajeError(detail, "No se pudo completar el registro."));
    } finally {
      setCargando(false);
    }
  }

  return (
    <form onSubmit={enviar} className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-3">
        <label className={estiloLabel}>
          Nombre
          <input
            required
            value={form.first_name}
            onChange={(e) => actualizar("first_name", e.target.value)}
            className={estiloInput}
          />
        </label>
        <label className={estiloLabel}>
          Apellido
          <input
            required
            value={form.last_name}
            onChange={(e) => actualizar("last_name", e.target.value)}
            className={estiloInput}
          />
        </label>
      </div>
      <label className={estiloLabel}>
        Usuario
        <input
          required
          value={form.username}
          onChange={(e) => actualizar("username", e.target.value)}
          className={estiloInput}
        />
      </label>
      <label className={estiloLabel}>
        Correo electrónico
        <input
          type="email"
          required
          value={form.email}
          onChange={(e) => actualizar("email", e.target.value)}
          className={estiloInput}
        />
      </label>
      <label className={estiloLabel}>
        Teléfono (opcional)
        <input value={form.telefono} onChange={(e) => actualizar("telefono", e.target.value)} className={estiloInput} />
      </label>
      <label className={estiloLabel}>
        Contraseña
        <input
          type="password"
          required
          minLength={8}
          value={form.password}
          onChange={(e) => actualizar("password", e.target.value)}
          className={estiloInput}
        />
      </label>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button type="submit" disabled={cargando} className={estiloBoton}>
        {cargando ? "Creando cuenta..." : "Crear cuenta"}
      </button>
    </form>
  );
}

export function AuthModal({
  vista,
  onCambiarVista,
  onCerrar,
}: {
  vista: VistaAuth | null;
  onCambiarVista: (vista: VistaAuth) => void;
  onCerrar: () => void;
}) {
  return (
    <Modal abierto={vista !== null} onCerrar={onCerrar}>
      <div className="mb-5 flex gap-6 border-b border-[var(--border-subtle)]">
        <button
          type="button"
          onClick={() => onCambiarVista("login")}
          className={`-mb-px border-b-2 pb-3 text-sm font-semibold transition-colors ${
            vista === "login" ? "border-brand-500 text-brand-600" : "border-transparent text-[var(--foreground)]/50"
          }`}
        >
          Iniciar sesión
        </button>
        <button
          type="button"
          onClick={() => onCambiarVista("registro")}
          className={`-mb-px border-b-2 pb-3 text-sm font-semibold transition-colors ${
            vista === "registro" ? "border-brand-500 text-brand-600" : "border-transparent text-[var(--foreground)]/50"
          }`}
        >
          Crear cuenta
        </button>
      </div>

      {vista === "login" ? (
        <FormularioLogin onExito={onCerrar} />
      ) : (
        <FormularioRegistro onExito={onCerrar} />
      )}
    </Modal>
  );
}
