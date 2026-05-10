import { useState } from "react";
import { useParams } from "react-router-dom";
import { Plus, FileDown } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { EmptyState } from "@/components/shared/EmptyState";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { WeatherWidget } from "@/components/external/WeatherWidget";
import { useNotes, useCreateNote } from "@/hooks/useNotes";
import { useInvoice, useExportInvoice } from "@/hooks/useInvoice";
import { InvoiceHeader } from "@/components/invoice/InvoiceHeader";
import { InvoiceTable } from "@/components/invoice/InvoiceTable";
import { InvoiceSummary } from "@/components/invoice/InvoiceSummary";
import { formatDate } from "@/utils/dates";
import { useTrip } from "@/hooks/useTrips";

const TABS = ["Notes", "Weather", "Invoice"] as const;
type Tab = (typeof TABS)[number];

export default function TripInfo() {
  const { tripSlug } = useParams<{ tripSlug: string }>();
  const slug = tripSlug!;
  const [tab, setTab] = useState<Tab>("Notes");

  const { data: trip } = useTrip(slug);
  const { data: notes, isLoading: notesLoading } = useNotes(slug);
  const { data: invoice } = useInvoice(slug);
  const { mutate: exportPdf, isPending: exporting } = useExportInvoice(slug);

  return (
    <PageWrapper title="Trip Hub" description="Notes, weather, and finances for your trip.">
      <div className="flex gap-2 border-b mb-4">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`pb-2 px-3 text-sm border-b-2 transition-colors ${tab === t ? "border-primary font-medium text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Notes" && (
        <div className="flex flex-col gap-4">
          {notesLoading ? (
            <Spinner />
          ) : !notes?.length ? (
            <EmptyState title="No notes yet" description="Capture ideas, reminders, and travel thoughts." />
          ) : (
            notes.map((note) => (
              <div key={note.id} className="rounded-lg border p-4">
                {note.title && <p className="font-medium mb-1">{note.title}</p>}
                <p className="text-sm whitespace-pre-wrap">{note.content}</p>
                <p className="text-xs text-muted-foreground mt-2">{formatDate(note.created_at)}</p>
              </div>
            ))
          )}
        </div>
      )}

      {tab === "Weather" && (
        <div className="grid sm:grid-cols-2 gap-4">
          <WeatherWidget isLoading={false} cityName="Current stop" />
        </div>
      )}

      {tab === "Invoice" && (
        <div className="flex flex-col gap-4">
          {invoice ? (
            <>
              <div className="flex items-center justify-between">
                <InvoiceHeader invoice={invoice} tripTitle={trip?.title} />
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2"
                  onClick={() => exportPdf()}
                  disabled={exporting}
                >
                  <FileDown className="h-4 w-4" />
                  {exporting ? "Exporting…" : "Export PDF"}
                </Button>
              </div>
              <InvoiceTable invoice={invoice} tripSlug={slug} editable />
              <InvoiceSummary invoice={invoice} />
            </>
          ) : (
            <EmptyState title="No invoice yet" description="Create an invoice to track expenses." />
          )}
        </div>
      )}
    </PageWrapper>
  );
}
