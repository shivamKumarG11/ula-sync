import client from "./client";
import type {
  Invoice,
  InvoiceCreateInput,
  InvoiceItemCreateInput,
} from "@/types/invoice";

const base = (tripSlug: string) => `/api/v1/trips/${tripSlug}/invoice`;

export const invoiceApi = {
  get: (tripSlug: string) => client.get<Invoice>(base(tripSlug)),

  create: (tripSlug: string, data: InvoiceCreateInput) =>
    client.post<Invoice>(base(tripSlug), data),

  update: (tripSlug: string, data: Partial<InvoiceCreateInput>) =>
    client.put<Invoice>(base(tripSlug), data),

  addItem: (tripSlug: string, data: InvoiceItemCreateInput) =>
    client.post(`${base(tripSlug)}/items`, data),

  updateItem: (tripSlug: string, itemId: number, data: Partial<InvoiceItemCreateInput>) =>
    client.put(`${base(tripSlug)}/items/${itemId}`, data),

  deleteItem: (tripSlug: string, itemId: number) =>
    client.delete(`${base(tripSlug)}/items/${itemId}`),

  exportPdf: (tripSlug: string) =>
    client.get(`${base(tripSlug)}/export`, { responseType: "blob" }),
};
