import {
  Beef,
  ChefHat,
  Coffee,
  CookingPot,
  Fish,
  Globe,
  Salad,
  Soup,
  type LucideIcon,
} from "lucide-react";

export interface CategoriaInfo {
  valor: string;
  etiqueta: string;
  icono: LucideIcon;
}

export const CATEGORIAS: CategoriaInfo[] = [
  { valor: "paraguaya", etiqueta: "Comida Paraguaya", icono: ChefHat },
  { valor: "parrilla", etiqueta: "Parrilla y Asado", icono: Beef },
  { valor: "internacional", etiqueta: "Internacional", icono: Globe },
  { valor: "mariscos", etiqueta: "Mariscos y Pescados", icono: Fish },
  { valor: "vegetariana", etiqueta: "Vegetariana", icono: Salad },
  { valor: "italiana", etiqueta: "Italiana", icono: CookingPot },
  { valor: "japonesa", etiqueta: "Japonesa", icono: Soup },
  { valor: "cafeteria", etiqueta: "Cafetería y Confitería", icono: Coffee },
];

export function obtenerIconoCategoria(valor: string): LucideIcon {
  return CATEGORIAS.find((c) => c.valor === valor)?.icono ?? ChefHat;
}

export const CIUDADES = ["Asunción", "Encarnación", "Ciudad del Este"];

export const RANGOS_PRECIO = [
  { valor: "$", etiqueta: "$ Económico" },
  { valor: "$$", etiqueta: "$$ Moderado" },
  { valor: "$$$", etiqueta: "$$$ Alto" },
  { valor: "$$$$", etiqueta: "$$$$ Premium" },
];
