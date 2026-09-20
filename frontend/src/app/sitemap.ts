import type { MetadataRoute } from "next";

import { apiFetch } from "@/lib/api";
import { SITE_URL } from "@/lib/site";
import type { Paginado, Restaurante } from "@/types";

async function obtenerSlugs(): Promise<string[]> {
  const slugs: string[] = [];
  let pagina = 1;
  try {
    // El listado pagina de a 12: hay que recorrer todas las páginas para no
    // dejar restaurantes fuera del sitemap.
    while (true) {
      const data = await apiFetch<Paginado<Restaurante>>(`/restaurantes/?page=${pagina}`, {
        cache: "no-store",
      });
      slugs.push(...data.results.map((restaurante) => restaurante.slug));
      if (!data.next) break;
      pagina += 1;
    }
  } catch {
    // Si la API no responde, el sitemap se sirve solo con las rutas estáticas.
  }
  return slugs;
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const slugs = await obtenerSlugs();
  const ahora = new Date();

  const rutasEstaticas: MetadataRoute.Sitemap = [
    { url: SITE_URL, lastModified: ahora, changeFrequency: "daily", priority: 1 },
    {
      url: `${SITE_URL}/restaurantes`,
      lastModified: ahora,
      changeFrequency: "daily",
      priority: 0.9,
    },
    { url: `${SITE_URL}/nosotros`, lastModified: ahora, changeFrequency: "monthly", priority: 0.4 },
  ];

  const rutasRestaurantes: MetadataRoute.Sitemap = slugs.map((slug) => ({
    url: `${SITE_URL}/restaurantes/${slug}`,
    lastModified: ahora,
    changeFrequency: "weekly",
    priority: 0.7,
  }));

  return [...rutasEstaticas, ...rutasRestaurantes];
}
