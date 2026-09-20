import type { Metadata } from "next";

import { MisReservasView } from "./MisReservasView";

export const metadata: Metadata = {
  title: "Mis reservas",
  description: "Consulta, revisa y cancela tus reservas en ReservaYa.",
  robots: { index: false, follow: false },
};

export default function MisReservasPage() {
  return <MisReservasView />;
}
