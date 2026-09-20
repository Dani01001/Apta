import type { Metadata, Viewport } from "next";
import { Fraunces, Inter } from "next/font/google";

import { Footer } from "@/components/Footer";
import { Navbar } from "@/components/Navbar";
import { AuthProvider } from "@/lib/auth-context";
import { AuthModalProvider } from "@/lib/auth-modal-context";
import { SITE_URL } from "@/lib/site";

import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});

const TITULO = "ReservaYa — Reserva tu mesa favorita";
const DESCRIPCION =
  "Encuentra y reserva mesa en los mejores restaurantes de Asunción, Encarnación y Ciudad del Este. Un producto de Apta.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: TITULO,
    template: "%s · ReservaYa",
  },
  description: DESCRIPCION,
  keywords: [
    "reservar restaurante Paraguay",
    "reservas Asunción",
    "restaurantes Encarnación",
    "restaurantes Ciudad del Este",
    "ReservaYa",
    "Apta",
  ],
  authors: [{ name: "Apta" }],
  openGraph: {
    type: "website",
    locale: "es_PY",
    siteName: "ReservaYa",
    title: TITULO,
    description: DESCRIPCION,
    url: SITE_URL,
  },
  twitter: {
    card: "summary_large_image",
    title: TITULO,
    description: DESCRIPCION,
  },
};

export const viewport: Viewport = {
  themeColor: "#d6472a",
  colorScheme: "light",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={`${inter.variable} ${fraunces.variable} antialiased`}>
        <AuthProvider>
          <AuthModalProvider>
            <div className="flex min-h-screen flex-col">
              <Navbar />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
          </AuthModalProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
