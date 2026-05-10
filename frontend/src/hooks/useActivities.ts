import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { activitiesApi } from "@/api/activities";
import type { StopActivityCreateInput } from "@/types/activity";

export function useCityActivities(citySlug: string, params?: { category?: string; page?: number }) {
  return useQuery({
    queryKey: ["city-activities", citySlug, params],
    queryFn: () => activitiesApi.listByCity(citySlug, params).then((r) => r.data),
    enabled: !!citySlug,
  });
}

export function useStopActivities(tripSlug: string, stopId: number) {
  return useQuery({
    queryKey: ["stop-activities", tripSlug, stopId],
    queryFn: () => activitiesApi.listByStop(tripSlug, stopId).then((r) => r.data),
    enabled: !!tripSlug && !!stopId,
  });
}

export function useAddStopActivity(tripSlug: string, stopId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: StopActivityCreateInput) =>
      activitiesApi.addToStop(tripSlug, stopId, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["stop-activities", tripSlug, stopId] }),
  });
}

export function useToggleActivityComplete(tripSlug: string, stopId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ activityId, is_completed }: { activityId: number; is_completed: boolean }) =>
      activitiesApi.updateStopActivity(tripSlug, stopId, activityId, { is_completed }),
    onMutate: async ({ activityId, is_completed }) => {
      await qc.cancelQueries({ queryKey: ["stop-activities", tripSlug, stopId] });
      const prev = qc.getQueryData(["stop-activities", tripSlug, stopId]);
      qc.setQueryData(["stop-activities", tripSlug, stopId], (old: unknown) => {
        if (!Array.isArray(old)) return old;
        return old.map((a: { id: number; is_completed: boolean }) =>
          a.id === activityId ? { ...a, is_completed } : a,
        );
      });
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      if (ctx?.prev) qc.setQueryData(["stop-activities", tripSlug, stopId], ctx.prev);
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ["stop-activities", tripSlug, stopId] }),
  });
}

export function useRemoveStopActivity(tripSlug: string, stopId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (activityId: number) => activitiesApi.removeFromStop(tripSlug, stopId, activityId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["stop-activities", tripSlug, stopId] }),
  });
}
