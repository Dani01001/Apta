"use client";

import { CalendarCheck, CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { Modal } from "@/components/Modal";
import { ApiError, apiFetch, extraerMensajeError } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { useAuthModal } from "@/lib/auth-modal-context";
import type { Reserva } from "@/types";

function manana(): string {
  const fecha = new Date();
  fecha.setDate(fecha.getDate() + 1);
  return fecha.toISOString().split("T")[0];
}

function horariosDisponibles(apertura: string, cierre: string): string[] {
  const [horaInicio, minInicio] = apertura.split(":").map(Number);
  const [horaFin, minFin] = cierre.split(":").map(Number);
  const inicio = horaInicio * 60 + minInicio;
  const fin = horaFin * 60 + minFin;
  const horarios: string[] = [];
  for (let minutos = inicio; minutos <= fin; minutos += 30) {
    const h = String(Math.floor(minutos / 60)).padStart(2, "0");
    const m = String(minutos % 60).padStart(2, "0");
    horarios.push(`${h}:${m}`);
  }
  return horarios;
}

export function ReservationForm({
  restauranteId,
  restauranteNombre,
  capacidad,
  horaApertura,
  horaCierre,
}: {
  restauranteId: number;
  restauranteNombre: string;
  capacidad: number;
  horaApertura: string;
  horaCierre: string;
}) {
  const { usuario, access, logout } = useAuth();
  const { abrirLogin } = useAuthModal();
  const horarios = horariosDisponibles(horaApertura, horaCierre);
  const horaPorDefecto = horarios.includes("20:00")
    ? "20:00"
    : horarios[Math.floor(horarios.length / 2)];
  const [fecha, setFecha] = useState(manana());
  const [hora, setHora] = useState(horaPorDefecto);
  const [personas, setPersonas] = useState(2);
  const [notas, setNotas] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<Reserva | null>(null);

  if (!usuario || !access) {
    return (
      <div className="rounded-2xl border border-[var(--border-subtle)] bg-brand-50 p-6 text-center">
        <p className="mb-4 text-sm font-medium text-[var(--foreground)]/80">
          Inicia sesión para reservar una mesa en este restaurante.
        </p>
        <button
          onClick={abrirLogin}
          className="inline-block rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-brand-600"
        >
          Iniciar sesión
        </button>
      </div>
    );
  }

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      const reserva = await apiFetch<Reserva>("/reservas/", {
        method: "POST",
        token: access,
        body: JSON.stringify({
          restaurante: restauranteId,
          fecha,
          hora,
          numero_personas: personas,
          notas,
        }),
      });
      setExito(reserva);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        logout();
        setError("Tu sesión expiró. Iniciá sesión de nuevo para confirmar la reserva.");
        abrirLogin();
      } else {
        const detail = err instanceof ApiError ? err.detail : undefined;
        setError(extraerMensajeError(detail, "No se pudo crear la reserva."));
      }
    } finally {
      setEnviando(false);
    }
  }

  return (
    <>
      <form
        onSubmit={enviar}
        className="flex flex-col gap-4 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-6"
      >
        <h3 className="font-display text-lg font-semibold">Reservar mesa</h3>

        <div className="grid grid-cols-2 gap-3">
          <label className="flex flex-col gap-1 text-sm">
            Fecha
            <input
              type="date"
              required
              min={new Date().toISOString().split("T")[0]}
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              className="rounded-lg border border-[var(--border-subtle)] bg-transparent px-3 py-2 outline-none focus:border-brand-400"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            Hora
            <select
              required
              value={hora}
              onChange={(e) => setHora(e.target.value)}
              className="rounded-lg border border-[var(--border-subtle)] bg-transparent px-3 py-2 outline-none focus:border-brand-400"
            >
              {horarios.map((h) => (
                <option key={h} value={h}>
                  {h}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label className="flex flex-col gap-1 text-sm">
          Número de personas
          <input
            type="number"
            min={1}
            max={Math.min(capacidad, 20)}
            required
            value={personas}
            onChange={(e) => setPersonas(Number(e.target.value))}
            className="rounded-lg border border-[var(--border-subtle)] bg-transparent px-3 py-2 outline-none focus:border-brand-400"
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          Notas (opcional)
          <textarea
            value={notas}
            onChange={(e) => setNotas(e.target.value)}
            rows={2}
            maxLength={280}
            placeholder="Alguna preferencia especial..."
            className="resize-none rounded-lg border border-[var(--border-subtle)] bg-transparent px-3 py-2 outline-none focus:border-brand-400"
          />
        </label>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={enviando}
          className="rounded-full bg-brand-500 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-brand-600 disabled:opacity-60"
        >
          {enviando ? "Reservando..." : "Confirmar reserva"}
        </button>
      </form>

      <Modal abierto={exito !== null} onCerrar={() => setExito(null)} ancho="sm">
        {exito && (
          <div className="text-center">
            <span className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-green-600">
              <CheckCircle2 className="h-7 w-7" />
            </span>
            <h2 className="mb-1 font-display text-xl font-semibold">Reserva creada</h2>
            <p className="mb-1 text-sm text-[var(--foreground)]/70">{restauranteNombre}</p>
            <p className="mb-5 text-sm text-[var(--foreground)]/70">
              {exito.fecha} a las {exito.hora.slice(0, 5)} para {exito.numero_personas} personas
              <br />
              Estado: {exito.estado_display}
            </p>
            <Link
              href="/mis-reservas"
              className="inline-flex items-center gap-2 rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-brand-600"
            >
              <CalendarCheck className="h-4 w-4" />
              Ver mis reservas
            </Link>
          </div>
        )}
      </Modal>
    </>
  );
}
