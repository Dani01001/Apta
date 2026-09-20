"use client";

import { AlertTriangle, CalendarX2 } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import { Modal } from "@/components/Modal";
import { ApiError, apiFetch } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { useAuthModal } from "@/lib/auth-modal-context";
import type { Paginado, Reserva } from "@/types";

const ESTILOS_ESTADO: Record<string, string> = {
  pendiente: "bg-amber-100 text-amber-800",
  confirmada: "bg-green-100 text-green-800",
  cancelada: "bg-red-100 text-red-800",
  completada: "bg-gray-200 text-gray-700",
};

export function MisReservasView() {
  const { usuario, access, logout, cargando: cargandoAuth } = useAuth();
  const { abrirLogin } = useAuthModal();
  const [reservas, setReservas] = useState<Reserva[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [cancelando, setCancelando] = useState<number | null>(null);
  const [reservaAConfirmar, setReservaAConfirmar] = useState<Reserva | null>(null);

  const cargarReservas = useCallback(async () => {
    if (!access) return;
    try {
      const data = await apiFetch<Paginado<Reserva>>("/reservas/", { token: access });
      setReservas(data.results);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        logout();
        setError("Tu sesión expiró. Iniciá sesión de nuevo para ver tus reservas.");
        abrirLogin();
      } else {
        setError("No se pudieron cargar tus reservas.");
      }
    }
  }, [access, logout, abrirLogin]);

  useEffect(() => {
    if (cargandoAuth || !usuario) return;
    // Carga las reservas del usuario contra la API una vez que la sesión está lista.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    cargarReservas();
  }, [usuario, cargandoAuth, cargarReservas]);

  async function confirmarCancelacion() {
    if (!access || !reservaAConfirmar) return;
    const id = reservaAConfirmar.id;
    setCancelando(id);
    try {
      await apiFetch(`/reservas/${id}/cancelar/`, {
        method: "PATCH",
        token: access,
        body: JSON.stringify({}),
      });
      setReservas((prev) =>
        prev
          ? prev.map((r) =>
              r.id === id ? { ...r, estado: "cancelada", estado_display: "Cancelada" } : r
            )
          : prev
      );
      setReservaAConfirmar(null);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        logout();
        setError("Tu sesión expiró. Iniciá sesión de nuevo para cancelar la reserva.");
        abrirLogin();
      } else {
        setError("No se pudo cancelar la reserva.");
      }
    } finally {
      setCancelando(null);
    }
  }

  if (cargandoAuth) {
    return <div className="mx-auto max-w-4xl px-4 py-16 text-center text-[var(--foreground)]/60">Cargando...</div>;
  }

  if (!usuario) {
    return (
      <div className="mx-auto max-w-md px-4 py-20 text-center">
        <h1 className="mb-3 font-display text-2xl font-semibold">Mis reservas</h1>
        <p className="mb-6 text-[var(--foreground)]/70">
          Inicia sesión para ver y gestionar tus reservas en ReservaYa.
        </p>
        <button
          onClick={abrirLogin}
          className="rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-brand-600"
        >
          Iniciar sesión
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <h1 className="mb-2 font-display text-3xl font-semibold">Mis reservas</h1>
      <p className="mb-8 text-[var(--foreground)]/70">
        Hola {usuario.first_name || usuario.username}, aquí puedes ver y gestionar tus reservas.
      </p>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

      {reservas === null ? (
        <p className="text-[var(--foreground)]/60">Cargando reservas...</p>
      ) : reservas.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-[var(--border-subtle)] p-10 text-center">
          <p className="mb-4 text-[var(--foreground)]/70">Todavía no tienes reservas.</p>
          <Link
            href="/restaurantes"
            className="inline-block rounded-full bg-brand-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-brand-600"
          >
            Explorar restaurantes
          </Link>
        </div>
      ) : (
        <ul className="flex flex-col gap-4">
          {reservas.map((reserva) => (
            <li
              key={reserva.id}
              className="flex flex-col gap-4 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)] p-4 sm:flex-row sm:items-center"
            >
              <div className="relative h-24 w-full shrink-0 overflow-hidden rounded-xl bg-brand-100 sm:w-32">
                <Image
                  src={reserva.restaurante_detalle.imagen_url}
                  alt={reserva.restaurante_detalle.nombre}
                  fill
                  sizes="128px"
                  className="object-cover"
                />
              </div>

              <div className="flex-1">
                <Link
                  href={`/restaurantes/${reserva.restaurante_detalle.slug}`}
                  className="font-display text-lg font-semibold hover:text-brand-600"
                >
                  {reserva.restaurante_detalle.nombre}
                </Link>
                <p className="text-sm text-[var(--foreground)]/60">
                  {reserva.fecha} · {reserva.hora.slice(0, 5)} · {reserva.numero_personas} personas
                </p>
                {reserva.notas && (
                  <p className="mt-1 text-sm text-[var(--foreground)]/50 italic">
                    &ldquo;{reserva.notas}&rdquo;
                  </p>
                )}
              </div>

              <div className="flex items-center gap-3">
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    ESTILOS_ESTADO[reserva.estado] ?? "bg-gray-100 text-gray-700"
                  }`}
                >
                  {reserva.estado_display}
                </span>
                {(reserva.estado === "pendiente" || reserva.estado === "confirmada") && (
                  <button
                    onClick={() => setReservaAConfirmar(reserva)}
                    className="rounded-full border border-[var(--border-subtle)] px-4 py-1.5 text-xs font-medium hover:border-red-400 hover:text-red-600"
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      <Modal
        abierto={reservaAConfirmar !== null}
        onCerrar={() => setReservaAConfirmar(null)}
        ancho="sm"
      >
        {reservaAConfirmar && (
          <div className="text-center">
            <span className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-100 text-red-600">
              <AlertTriangle className="h-7 w-7" />
            </span>
            <h2 className="mb-1 font-display text-xl font-semibold">¿Cancelar esta reserva?</h2>
            <p className="mb-6 text-sm text-[var(--foreground)]/70">
              {reservaAConfirmar.restaurante_detalle.nombre} · {reservaAConfirmar.fecha} a las{" "}
              {reservaAConfirmar.hora.slice(0, 5)}. Esta acción no se puede deshacer.
            </p>
            <div className="flex justify-center gap-3">
              <button
                onClick={() => setReservaAConfirmar(null)}
                className="rounded-full border border-[var(--border-subtle)] px-5 py-2 text-sm font-medium hover:bg-black/5"
              >
                Volver
              </button>
              <button
                onClick={confirmarCancelacion}
                disabled={cancelando !== null}
                className="flex items-center gap-2 rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white hover:bg-red-700 disabled:opacity-60"
              >
                <CalendarX2 className="h-4 w-4" />
                {cancelando !== null ? "Cancelando..." : "Sí, cancelar"}
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
