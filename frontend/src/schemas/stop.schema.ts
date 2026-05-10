import { z } from "zod";

export const stopSchema = z.object({
  city_id: z.number().int().positive("Select a city"),
  arrival_date: z.string().optional(),
  departure_date: z.string().optional(),
  nights: z.number().int().min(0).optional(),
  accommodation_name: z.string().max(200).optional(),
  accommodation_url: z.string().url("Must be a valid URL").optional().or(z.literal("")),
  notes: z.string().max(1000).optional(),
});

export type StopFormInput = z.infer<typeof stopSchema>;
