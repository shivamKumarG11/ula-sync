import { z } from "zod";

export const invoiceSchema = z.object({
  title: z.string().max(200).optional(),
  notes: z.string().max(500).optional(),
  currency: z.string().length(3).default("USD"),
  tax_rate: z.number().min(0).max(100).default(0),
  discount_usd: z.number().min(0).default(0),
});

export const invoiceItemSchema = z.object({
  description: z.string().min(1, "Description required").max(200),
  category: z.string().max(50).default("general"),
  quantity: z.number().int().min(1).default(1),
  unit_price_usd: z.number().min(0, "Price must be non-negative"),
});

export type InvoiceFormInput = z.infer<typeof invoiceSchema>;
export type InvoiceItemFormInput = z.infer<typeof invoiceItemSchema>;
