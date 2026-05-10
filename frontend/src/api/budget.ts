import client from "./client";
import type { BudgetSummary } from "@/types/budget";

export const budgetApi = {
  get: (tripSlug: string) =>
    client.get<BudgetSummary>(`/api/v1/trips/${tripSlug}/budget`),
};
