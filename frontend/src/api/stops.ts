import client from "./client";
import type { Stop, StopCreateInput, StopUpdateInput, ReorderInput } from "@/types/stop";

const base = (tripSlug: string) => `/api/v1/trips/${tripSlug}/stops`;

export const stopsApi = {
  list: (tripSlug: string) => client.get<Stop[]>(base(tripSlug)),

  add: (tripSlug: string, data: StopCreateInput) =>
    client.post<Stop>(base(tripSlug), data),

  reorder: (tripSlug: string, data: ReorderInput) =>
    client.put<Stop[]>(`${base(tripSlug)}/reorder`, data),

  update: (tripSlug: string, stopId: number, data: StopUpdateInput) =>
    client.put<Stop>(`${base(tripSlug)}/${stopId}`, data),

  delete: (tripSlug: string, stopId: number) =>
    client.delete(`${base(tripSlug)}/${stopId}`),
};
