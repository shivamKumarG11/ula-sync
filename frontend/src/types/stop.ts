export interface Stop {
  id: number;
  trip_id: number;
  city_id: number;
  city_name: string;
  city_slug: string;
  city_country: string;
  city_cover_url: string | null;
  order_index: number;
  arrival_date: string | null;
  departure_date: string | null;
  nights: number | null;
  accommodation_name: string | null;
  accommodation_url: string | null;
  notes: string | null;
  created_at: string;
}

export interface StopCreateInput {
  city_id: number;
  arrival_date?: string;
  departure_date?: string;
  nights?: number;
  accommodation_name?: string;
  accommodation_url?: string;
  notes?: string;
}

export interface StopUpdateInput extends Partial<StopCreateInput> {}

export interface ReorderInput {
  ordered_ids: number[];
}
