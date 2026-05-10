import { z } from "zod";

export const packingItemSchema = z.object({
  name: z.string().min(1, "Item name is required").max(120),
  category: z
    .enum(["clothing", "toiletries", "electronics", "documents", "health", "accessories", "other"])
    .default("other"),
  quantity: z.number().int().min(1).default(1),
  is_essential: z.boolean().default(false),
  notes: z.string().max(300).optional(),
});

export type PackingItemFormInput = z.infer<typeof packingItemSchema>;
