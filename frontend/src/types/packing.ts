export type PackingCategory =
  | "clothing"
  | "toiletries"
  | "electronics"
  | "documents"
  | "health"
  | "accessories"
  | "other";

export interface PackingItem {
  id: number;
  trip_id: number;
  stop_id: number | null;
  name: string;
  category: PackingCategory;
  quantity: number;
  is_packed: boolean;
  is_essential: boolean;
  notes: string | null;
}

export interface PackingItemCreateInput {
  name: string;
  category?: PackingCategory;
  quantity?: number;
  is_essential?: boolean;
  stop_id?: number;
  notes?: string;
}

export interface PackingItemUpdateInput extends Partial<PackingItemCreateInput> {
  is_packed?: boolean;
}

export interface PackingProgress {
  total: number;
  packed: number;
  percentage: number;
}
