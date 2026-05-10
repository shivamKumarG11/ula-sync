import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { stopsApi } from "@/api/stops";
import type { StopCreateInput, StopUpdateInput, ReorderInput } from "@/types/stop";

export function useStops(tripSlug: string) {
  return useQuery({
    queryKey: ["stops", tripSlug],
    queryFn: () => stopsApi.list(tripSlug).then((r) => r.data),
    enabled: !!tripSlug,
  });
}

export function useAddStop(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: StopCreateInput) => stopsApi.add(tripSlug, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["stops", tripSlug] }),
  });
}

export function useReorderStops(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ReorderInput) => stopsApi.reorder(tripSlug, data).then((r) => r.data),
    onMutate: async (data) => {
      await qc.cancelQueries({ queryKey: ["stops", tripSlug] });
      const prev = qc.getQueryData(["stops", tripSlug]);
      return { prev };
    },
    onError: (_err, _data, ctx) => {
      if (ctx?.prev) qc.setQueryData(["stops", tripSlug], ctx.prev);
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ["stops", tripSlug] }),
  });
}

export function useUpdateStop(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ stopId, data }: { stopId: number; data: StopUpdateInput }) =>
      stopsApi.update(tripSlug, stopId, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["stops", tripSlug] }),
  });
}

export function useDeleteStop(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (stopId: number) => stopsApi.delete(tripSlug, stopId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["stops", tripSlug] }),
  });
}
