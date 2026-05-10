export interface BudgetCategoryBreakdown {
  category: string;
  total_usd: number;
  percentage: number;
}

export interface BudgetStopBreakdown {
  stop_id: number;
  city_name: string;
  total_usd: number;
  days: number;
  daily_usd: number;
}

export interface BudgetSummary {
  trip_slug: string;
  budget_total_usd: number | null;
  estimated_total_usd: number;
  remaining_usd: number | null;
  per_day_usd: number | null;
  per_person_usd: number | null;
  total_days: number;
  traveler_count: number;
  by_category: BudgetCategoryBreakdown[];
  by_stop: BudgetStopBreakdown[];
}
