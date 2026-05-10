export interface InvoiceItem {
  id: number;
  invoice_id: number;
  description: string;
  category: string;
  quantity: number;
  unit_price_usd: number;
  line_total_usd: number;
}

export interface Invoice {
  id: number;
  trip_id: number;
  invoice_number: string;
  title: string | null;
  notes: string | null;
  currency: string;
  subtotal_usd: number;
  tax_rate: number;
  tax_usd: number;
  discount_usd: number;
  grand_total_usd: number;
  status: "draft" | "final";
  issued_date: string | null;
  items: InvoiceItem[];
  created_at: string;
}

export interface InvoiceCreateInput {
  title?: string;
  notes?: string;
  currency?: string;
  tax_rate?: number;
  discount_usd?: number;
}

export interface InvoiceItemCreateInput {
  description: string;
  category?: string;
  quantity?: number;
  unit_price_usd: number;
}
