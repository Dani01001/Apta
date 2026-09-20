export default function CargandoRestaurantes() {
  return (
    <div className="mx-auto max-w-6xl animate-pulse px-4 py-10 sm:px-6">
      <div className="mb-2 h-8 w-48 rounded-full bg-[var(--border-subtle)]" />
      <div className="mb-6 h-5 w-96 max-w-full rounded-full bg-[var(--border-subtle)]" />
      <div className="h-20 rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)]" />
      <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="overflow-hidden rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface)]"
          >
            <div className="aspect-[4/3] w-full bg-[var(--border-subtle)]" />
            <div className="flex flex-col gap-2 p-4">
              <div className="h-5 w-3/4 rounded-full bg-[var(--border-subtle)]" />
              <div className="h-4 w-full rounded-full bg-[var(--border-subtle)]" />
              <div className="h-4 w-2/3 rounded-full bg-[var(--border-subtle)]" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
