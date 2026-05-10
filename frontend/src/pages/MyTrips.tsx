import { useState } from "react";
import { Link } from "react-router-dom";
import { PlusCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { TripCard } from "@/components/trip/TripCard";
import { Skeleton } from "@/components/ui/Skeleton";
import { EmptyState } from "@/components/shared/EmptyState";
import { Pagination } from "@/components/shared/Pagination";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useAuth } from "@/hooks/useAuth";
import { useTrips } from "@/hooks/useTrips";

const STATUS_TABS = ["all", "planning", "active", "completed"] as const;

export default function MyTrips() {
  const { user } = useAuth();
  const [page, setPage] = useState(1);
  const [status, setStatus] = useState<string>("all");
  const { data, isLoading } = useTrips({
    page,
    per_page: 9,
    status: status === "all" ? undefined : status,
  });

  return (
    <PageWrapper
      title="My Trips"
      actions={
        <Link to={`/u/${user?.username}/trips/new`}>
          <Button className="gap-2">
            <PlusCircle className="h-4 w-4" /> New trip
          </Button>
        </Link>
      }
    >
      <div className="flex gap-2 border-b">
        {STATUS_TABS.map((t) => (
          <button
            key={t}
            onClick={() => { setStatus(t); setPage(1); }}
            className={`pb-2 px-3 text-sm capitalize border-b-2 transition-colors ${status === t ? "border-primary font-medium text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}
          >
            {t}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      ) : data?.items?.length ? (
        <>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.items.map((trip) => (
              <TripCard key={trip.id} trip={trip} />
            ))}
          </div>
          <Pagination
            page={data.page}
            pages={data.pages}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState
          title="No trips found"
          description={status !== "all" ? `No ${status} trips.` : "Create your first trip to get started."}
          action={
            <Link to={`/u/${user?.username}/trips/new`}>
              <Button>Create a trip</Button>
            </Link>
          }
        />
      )}
    </PageWrapper>
  );
}
