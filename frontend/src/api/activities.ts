import client from "./client";
import type { Activity, StopActivity, StopActivityCreateInput } from "@/types/activity";
import type { PaginatedResponse } from "@/types/api";

export const activitiesApi = {
  listByCity: (citySlug: string, params?: { category?: string; page?: number }) =>
    client.get<PaginatedResponse<Activity>>(`/api/v1/cities/${citySlug}/activities`, { params }),

  listByStop: (tripSlug: string, stopId: number) =>
    client.get<StopActivity[]>(`/api/v1/trips/${tripSlug}/stops/${stopId}/activities`),

  addToStop: (tripSlug: string, stopId: number, data: StopActivityCreateInput) =>
    client.post<StopActivity>(
      `/api/v1/trips/${tripSlug}/stops/${stopId}/activities`,
      data,
    ),

  updateStopActivity: (
    tripSlug: string,
    stopId: number,
    activityId: number,
    data: Partial<StopActivityCreateInput> & { is_completed?: boolean },
  ) =>
    client.put<StopActivity>(
      `/api/v1/trips/${tripSlug}/stops/${stopId}/activities/${activityId}`,
      data,
    ),

  removeFromStop: (tripSlug: string, stopId: number, activityId: number) =>
    client.delete(`/api/v1/trips/${tripSlug}/stops/${stopId}/activities/${activityId}`),
};
