import client from "./client";
import type { Trip, TripCreateInput, TripUpdateInput } from "@/types/trip";
import type { PaginatedResponse } from "@/types/api";

export const tripsApi = {
  list: (params?: { page?: number; per_page?: number; status?: string }) =>
    client.get<PaginatedResponse<Trip>>("/api/v1/trips", { params }),

  create: (data: TripCreateInput) => client.post<Trip>("/api/v1/trips", data),

  get: (slug: string) => client.get<Trip>(`/api/v1/trips/${slug}`),

  update: (slug: string, data: TripUpdateInput) =>
    client.put<Trip>(`/api/v1/trips/${slug}`, data),

  delete: (slug: string) => client.delete(`/api/v1/trips/${slug}`),

  share: (slug: string) => client.post<{ share_token: string }>(`/api/v1/trips/${slug}/share`),

  unshare: (slug: string) => client.delete(`/api/v1/trips/${slug}/share`),

  getShared: (token: string) => client.get<Trip>(`/api/v1/trips/shared/${token}`),

  uploadCover: (slug: string, file: File) => {
    const form = new FormData();
    form.append("cover_photo", file);
    return client.post(`/api/v1/trips/${slug}/cover`, form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};
