export type ActivityCategory =
  | "sightseeing"
  | "food"
  | "adventure"
  | "shopping"
  | "wellness"
  | "cultural"
  | "other";

export interface Activity {
  id: number;
  city_id: number;
  name: string;
  description: string | null;
  category: ActivityCategory;
  cost_usd: number;
  duration_hours: number | null;
  map_link: string | null;
  opening_time: string | null;
  closing_time: string | null;
  booking_required: boolean;
  booking_link: string | null;
}

export interface StopActivity {
  id: number;
  stop_id: number;
  activity_id: number;
  activity: Activity;
  order_index: number;
  scheduled_date: string | null;
  scheduled_time: string | null;
  notes: string | null;
  is_completed: boolean;
  cost_override_usd: number | null;
}

export interface StopActivityCreateInput {
  activity_id: number;
  scheduled_date?: string;
  scheduled_time?: string;
  notes?: string;
  cost_override_usd?: number;
}
