import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { notesApi } from "@/api/notes";
import type { NoteCreateInput, NoteUpdateInput } from "@/types/note";

export function useNotes(tripSlug: string, stopId?: number) {
  return useQuery({
    queryKey: ["notes", tripSlug, stopId],
    queryFn: () => notesApi.list(tripSlug, stopId).then((r) => r.data),
    enabled: !!tripSlug,
  });
}

export function useCreateNote(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: NoteCreateInput) => notesApi.create(tripSlug, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", tripSlug] }),
  });
}

export function useUpdateNote(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ noteId, data }: { noteId: number; data: NoteUpdateInput }) =>
      notesApi.update(tripSlug, noteId, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", tripSlug] }),
  });
}

export function useDeleteNote(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (noteId: number) => notesApi.delete(tripSlug, noteId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", tripSlug] }),
  });
}
