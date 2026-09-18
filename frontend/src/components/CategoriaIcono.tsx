import { obtenerIconoCategoria } from "@/lib/categorias";

export function CategoriaIcono({
  categoria,
  className,
}: {
  categoria: string;
  className?: string;
}) {
  // Selecciona un componente de ícono ya existente de una tabla estática (lucide-react);
  // nunca define un componente nuevo, por eso es seguro pese a la heurística del linter.
  /* eslint-disable react-hooks/static-components */
  const Icono = obtenerIconoCategoria(categoria);
  return <Icono className={className} />;
  /* eslint-enable react-hooks/static-components */
}
