import { useQuery } from "@tanstack/react-query";
import { citiesApi } from "@/api/cities";

export function useCities(params?: {
  q?: string;
  country?: string;
  page?: number;
  per_page?: number;
  sort?: string;
}) {
  return useQuery({
    queryKey: ["cities", params],
    queryFn: () => citiesApi.list(params).then((r) => r.data),
  });
}

export function useCity(slug: string) {
  return useQuery({
    queryKey: ["city", slug],
    queryFn: () => citiesApi.get(slug).then((r) => r.data),
    enabled: !!slug,
    staleTime: 10 * 60 * 1000,
  });
}

export function useSavedCities() {
  return useQuery({
    queryKey: ["saved-cities"],
    queryFn: () => citiesApi.savedList().then((r) => r.data),
  });
}
