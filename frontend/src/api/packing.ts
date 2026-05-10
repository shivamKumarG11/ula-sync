import client from "./client";
import type {
  PackingItem,
  PackingItemCreateInput,
  PackingItemUpdateInput,
} from "@/types/packing";

const base = (tripSlug: string) => `/api/v1/trips/${tripSlug}/packing`;

export const packingApi = {
  list: (tripSlug: string) => client.get<PackingItem[]>(base(tripSlug)),

  create: (tripSlug: string, data: PackingItemCreateInput) =>
    client.post<PackingItem>(base(tripSlug), data),

  batchCreate: (tripSlug: string, items: PackingItemCreateInput[]) =>
    client.post<PackingItem[]>(`${base(tripSlug)}/batch`, { items }),

  update: (tripSlug: string, itemId: number, data: PackingItemUpdateInput) =>
    client.put<PackingItem>(`${base(tripSlug)}/${itemId}`, data),

  delete: (tripSlug: string, itemId: number) =>
    client.delete(`${base(tripSlug)}/${itemId}`),

  seed: (tripSlug: string) => client.post<PackingItem[]>(`${base(tripSlug)}/seed`),

  reset: (tripSlug: string) => client.post(`${base(tripSlug)}/reset`),

  getShareToken: (tripSlug: string) =>
    client.get<{ share_token: string }>(`${base(tripSlug)}/share-token`),
};
