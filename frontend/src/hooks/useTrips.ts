import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { tripsApi } from "@/api/trips";
import type { TripCreateInput, TripUpdateInput } from "@/types/trip";

export function useTrips(params?: { page?: number; status?: string }) {
  return useQuery({
    queryKey: ["trips", params],
    queryFn: () => tripsApi.list(params).then((r) => r.data),
  });
}

export function useTrip(slug: string) {
  return useQuery({
    queryKey: ["trip", slug],
    queryFn: () => tripsApi.get(slug).then((r) => r.data),
    enabled: !!slug,
  });
}

export function useCreateTrip() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TripCreateInput) => tripsApi.create(data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["trips"] }),
  });
}

export function useUpdateTrip(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TripUpdateInput) => tripsApi.update(slug, data).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["trip", slug] });
      qc.invalidateQueries({ queryKey: ["trips"] });
    },
  });
}

export function useDeleteTrip() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (slug: string) => tripsApi.delete(slug),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["trips"] }),
  });
}

export function useShareTrip(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => tripsApi.share(slug).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["trip", slug] }),
  });
}
