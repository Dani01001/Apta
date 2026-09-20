import { ImageResponse } from "next/og";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 24,
          padding: "80px 96px",
          background: "linear-gradient(135deg, #fef3f0 0%, #fffaf3 45%, #fdf3e7 100%)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: 64,
              height: 64,
              borderRadius: 18,
              background: "#d6472a",
              color: "#fff",
              fontFamily: "serif",
              fontSize: 34,
              fontWeight: 700,
            }}
          >
            R
          </div>
          <div style={{ display: "flex", fontSize: 34, fontWeight: 700, color: "#93281a" }}>
            ReservaYa
          </div>
        </div>
        <div
          style={{
            display: "flex",
            fontFamily: "serif",
            fontSize: 64,
            fontWeight: 700,
            color: "#241a16",
            lineHeight: 1.15,
            maxWidth: 900,
          }}
        >
          Reserva tu mesa favorita en segundos
        </div>
        <div style={{ display: "flex", fontSize: 28, color: "#6f1f17" }}>
          Asunción · Encarnación · Ciudad del Este
        </div>
      </div>
    ),
    size
  );
}
