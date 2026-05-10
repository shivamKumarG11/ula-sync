import client from "./client";
import type { TripNote, NoteCreateInput, NoteUpdateInput } from "@/types/note";

const base = (tripSlug: string) => `/api/v1/trips/${tripSlug}/notes`;

export const notesApi = {
  list: (tripSlug: string, stopId?: number) =>
    client.get<TripNote[]>(base(tripSlug), { params: stopId ? { stop_id: stopId } : undefined }),

  create: (tripSlug: string, data: NoteCreateInput) =>
    client.post<TripNote>(base(tripSlug), data),

  update: (tripSlug: string, noteId: number, data: NoteUpdateInput) =>
    client.put<TripNote>(`${base(tripSlug)}/${noteId}`, data),

  delete: (tripSlug: string, noteId: number) =>
    client.delete(`${base(tripSlug)}/${noteId}`),
};
