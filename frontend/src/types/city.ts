export interface CityCostBreakdown {
  expense_type: string;
  cost_usd: number;
  cost_local: number;
  local_currency: string;
}

export interface City {
  id: number;
  slug: string;
  name: string;
  country: string;
  country_code: string | null;
  region: string | null;
  description: string | null;
  cover_photo_url: string | null;
  map_link: string | null;
  best_time_months: string | null;
  cost_index_usd: number | null;
  popularity_score: number | null;
  latitude: number | null;
  longitude: number | null;
  timezone: string | null;
  iata_code: string | null;
  wikipedia_title: string | null;
  cost_breakdown: CityCostBreakdown[];
}

export interface SavedCity {
  id: number;
  city_id: number;
  city: City;
  saved_at: string;
}
