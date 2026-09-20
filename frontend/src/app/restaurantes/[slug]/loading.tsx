export default function CargandoRestaurante() {
  return (
    <div className="mx-auto max-w-6xl animate-pulse px-4 py-10 sm:px-6">
      <div className="grid gap-8 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <div className="mb-6 aspect-video w-full rounded-2xl bg-[var(--border-subtle)]" />
          <div className="mb-4 h-6 w-48 rounded-full bg-[var(--border-subtle)]" />
          <div className="mb-3 h-9 w-2/3 rounded-full bg-[var(--border-subtle)]" />
          <div className="mb-2 h-4 w-full rounded-full bg-[var(--border-subtle)]" />
          <div className="mb-6 h-4 w-5/6 rounded-full bg-[var(--border-subtle)]" />
          <div className="h-40 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)]" />
        </div>
        <div className="h-96 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)]" />
      </div>
    </div>
  );
}
