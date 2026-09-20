import { ImageResponse } from "next/og";

export const size = { width: 32, height: 32 };
export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#d6472a",
          borderRadius: 8,
          fontFamily: "serif",
          fontSize: 20,
          fontWeight: 700,
          color: "#fff",
        }}
      >
        R
      </div>
    ),
    size
  );
}
