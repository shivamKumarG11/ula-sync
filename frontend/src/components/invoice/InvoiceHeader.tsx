import { DollarSign } from "lucide-react";
import type { Invoice } from "@/types/invoice";

interface InvoiceHeaderProps {
  invoice: Invoice;
  tripTitle?: string;
}

export function InvoiceHeader({ invoice, tripTitle }: InvoiceHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div>
        <h2 className="text-xl font-bold">{invoice.title ?? tripTitle ?? "Trip Invoice"}</h2>
        <p className="text-sm text-muted-foreground">#{invoice.invoice_number}</p>
      </div>
      <div className="text-right">
        <p className="text-2xl font-bold flex items-center gap-1 justify-end">
          <DollarSign className="h-5 w-5" />
          {invoice.grand_total_usd.toFixed(2)}
        </p>
        <p className="text-xs text-muted-foreground">{invoice.currency}</p>
      </div>
    </div>
  );
}
