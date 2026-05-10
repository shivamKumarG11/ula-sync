import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { formatCurrency } from "@/utils/formatters";
import { useDeleteInvoiceItem } from "@/hooks/useInvoice";
import type { Invoice } from "@/types/invoice";

interface InvoiceTableProps {
  invoice: Invoice;
  tripSlug: string;
  editable?: boolean;
}

export function InvoiceTable({ invoice, tripSlug, editable }: InvoiceTableProps) {
  const { mutate: deleteItem } = useDeleteInvoiceItem(tripSlug);

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left text-muted-foreground">
            <th className="pb-2 font-medium">Description</th>
            <th className="pb-2 font-medium">Category</th>
            <th className="pb-2 font-medium text-right">Qty</th>
            <th className="pb-2 font-medium text-right">Unit</th>
            <th className="pb-2 font-medium text-right">Total</th>
            {editable && <th className="pb-2 w-8" />}
          </tr>
        </thead>
        <tbody className="divide-y">
          {invoice.items.map((item) => (
            <tr key={item.id}>
              <td className="py-2">{item.description}</td>
              <td className="py-2 text-muted-foreground">{item.category}</td>
              <td className="py-2 text-right">{item.quantity}</td>
              <td className="py-2 text-right">{formatCurrency(item.unit_price_usd)}</td>
              <td className="py-2 text-right font-medium">{formatCurrency(item.line_total_usd)}</td>
              {editable && (
                <td className="py-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-muted-foreground hover:text-destructive"
                    onClick={() => deleteItem(item.id)}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
