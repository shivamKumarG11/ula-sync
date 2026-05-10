import { z } from "zod";

export const tripSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters").max(120),
  description: z.string().max(500).optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
  budget_total_usd: z.number().positive().optional(),
  currency: z.string().length(3).default("USD"),
  traveler_count: z.number().int().min(1).max(50).default(1),
  visibility: z.enum(["private", "public", "link_only"]).default("private"),
});

export type TripFormInput = z.infer<typeof tripSchema>;
