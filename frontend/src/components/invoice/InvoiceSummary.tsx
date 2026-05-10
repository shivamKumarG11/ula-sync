import { formatCurrency } from "@/utils/formatters";
import type { Invoice } from "@/types/invoice";

interface InvoiceSummaryProps {
  invoice: Invoice;
}

export function InvoiceSummary({ invoice }: InvoiceSummaryProps) {
  return (
    <div className="flex flex-col gap-1 text-sm ml-auto w-64">
      <div className="flex justify-between">
        <span className="text-muted-foreground">Subtotal</span>
        <span>{formatCurrency(invoice.subtotal_usd)}</span>
      </div>
      {invoice.tax_rate > 0 && (
        <div className="flex justify-between">
          <span className="text-muted-foreground">Tax ({invoice.tax_rate}%)</span>
          <span>{formatCurrency(invoice.tax_usd)}</span>
        </div>
      )}
      {invoice.discount_usd > 0 && (
        <div className="flex justify-between text-green-600">
          <span>Discount</span>
          <span>-{formatCurrency(invoice.discount_usd)}</span>
        </div>
      )}
      <div className="flex justify-between font-bold text-base border-t pt-1 mt-1">
        <span>Total</span>
        <span>{formatCurrency(invoice.grand_total_usd)}</span>
      </div>
    </div>
  );
}
