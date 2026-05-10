export type TripStatus = "planning" | "active" | "completed" | "cancelled";
export type TripVisibility = "private" | "public" | "link_only";

export interface Trip {
  id: number;
  slug: string;
  title: string;
  description: string | null;
  cover_photo_url: string | null;
  status: TripStatus;
  visibility: TripVisibility;
  start_date: string | null;
  end_date: string | null;
  budget_total_usd: number | null;
  currency: string;
  traveler_count: number;
  is_shared: boolean;
  share_token: string | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface TripCreateInput {
  title: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  budget_total_usd?: number;
  currency?: string;
  traveler_count?: number;
  visibility?: TripVisibility;
}

export interface TripUpdateInput extends Partial<TripCreateInput> {
  status?: TripStatus;
}
