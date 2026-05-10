import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { packingApi } from "@/api/packing";
import type { PackingItemCreateInput, PackingItemUpdateInput } from "@/types/packing";

export function usePacking(tripSlug: string) {
  return useQuery({
    queryKey: ["packing", tripSlug],
    queryFn: () => packingApi.list(tripSlug).then((r) => r.data),
    enabled: !!tripSlug,
  });
}

export function useCreatePackingItem(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: PackingItemCreateInput) =>
      packingApi.create(tripSlug, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["packing", tripSlug] }),
  });
}

export function useTogglePacked(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ itemId, is_packed }: { itemId: number; is_packed: boolean }) =>
      packingApi.update(tripSlug, itemId, { is_packed }),
    onMutate: async ({ itemId, is_packed }) => {
      await qc.cancelQueries({ queryKey: ["packing", tripSlug] });
      const prev = qc.getQueryData(["packing", tripSlug]);
      qc.setQueryData(["packing", tripSlug], (old: unknown) => {
        if (!Array.isArray(old)) return old;
        return old.map((item: { id: number; is_packed: boolean }) =>
          item.id === itemId ? { ...item, is_packed } : item,
        );
      });
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      if (ctx?.prev) qc.setQueryData(["packing", tripSlug], ctx.prev);
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ["packing", tripSlug] }),
  });
}

export function useUpdatePackingItem(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ itemId, data }: { itemId: number; data: PackingItemUpdateInput }) =>
      packingApi.update(tripSlug, itemId, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["packing", tripSlug] }),
  });
}

export function useDeletePackingItem(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: number) => packingApi.delete(tripSlug, itemId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["packing", tripSlug] }),
  });
}

export function useSeedPacking(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => packingApi.seed(tripSlug).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["packing", tripSlug] }),
  });
}
