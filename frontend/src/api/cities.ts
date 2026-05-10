import client from "./client";
import type { City, SavedCity } from "@/types/city";
import type { PaginatedResponse } from "@/types/api";

export const citiesApi = {
  list: (params?: {
    q?: string;
    country?: string;
    page?: number;
    per_page?: number;
    sort?: string;
  }) => client.get<PaginatedResponse<City>>("/api/v1/cities", { params }),

  get: (slug: string) => client.get<City>(`/api/v1/cities/${slug}`),

  savedList: () => client.get<SavedCity[]>("/api/v1/users/saved-cities"),

  save: (cityId: number) =>
    client.post<SavedCity>("/api/v1/users/saved-cities", { city_id: cityId }),

  unsave: (cityId: number) => client.delete(`/api/v1/users/saved-cities/${cityId}`),
};
