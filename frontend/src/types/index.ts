export interface Restaurante {
  id: number;
  nombre: string;
  slug: string;
  descripcion: string;
  categoria: string;
  categoria_display: string;
  ciudad: string;
  direccion: string;
  telefono: string;
  rango_precio: string;
  rango_precio_display: string;
  calificacion: string;
  capacidad: number;
  hora_apertura: string;
  hora_cierre: string;
  imagen_url: string;
  destacado: boolean;
}

export interface Paginado<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type EstadoReserva = "pendiente" | "confirmada" | "cancelada" | "completada";

export interface Reserva {
  id: number;
  restaurante: number;
  restaurante_detalle: Restaurante;
  fecha: string;
  hora: string;
  numero_personas: number;
  estado: EstadoReserva;
  estado_display: string;
  notas: string;
  creado_en: string;
}

export interface Perfil {
  telefono: string;
  foto_url: string;
}

export interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  perfil: Perfil;
}

export interface RespuestaAuth {
  access: string;
  refresh: string;
  usuario: Usuario;
}
