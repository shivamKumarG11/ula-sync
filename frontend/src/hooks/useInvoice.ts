import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { invoiceApi } from "@/api/invoice";
import type { InvoiceCreateInput, InvoiceItemCreateInput } from "@/types/invoice";

export function useInvoice(tripSlug: string) {
  return useQuery({
    queryKey: ["invoice", tripSlug],
    queryFn: () => invoiceApi.get(tripSlug).then((r) => r.data),
    enabled: !!tripSlug,
  });
}

export function useCreateInvoice(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: InvoiceCreateInput) => invoiceApi.create(tripSlug, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["invoice", tripSlug] }),
  });
}

export function useUpdateInvoice(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<InvoiceCreateInput>) =>
      invoiceApi.update(tripSlug, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["invoice", tripSlug] }),
  });
}

export function useAddInvoiceItem(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: InvoiceItemCreateInput) => invoiceApi.addItem(tripSlug, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["invoice", tripSlug] }),
  });
}

export function useDeleteInvoiceItem(tripSlug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: number) => invoiceApi.deleteItem(tripSlug, itemId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["invoice", tripSlug] }),
  });
}

export function useExportInvoice(tripSlug: string) {
  return useMutation({
    mutationFn: async () => {
      const res = await invoiceApi.exportPdf(tripSlug);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.download = `invoice-${tripSlug}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    },
  });
}
