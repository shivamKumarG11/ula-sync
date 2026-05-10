import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Pencil, Share2, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/shared/ErrorState";
import { TimelineView } from "@/components/trip/TimelineView";
import { BudgetChart } from "@/components/trip/BudgetChart";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useTrip } from "@/hooks/useTrips";
import { useStops } from "@/hooks/useStops";
import { useBudget } from "@/hooks/useBudget";
import { useAuth } from "@/hooks/useAuth";

export default function ItineraryView() {
  const { tripSlug } = useParams<{ tripSlug: string }>();
  const slug = tripSlug!;
  const { user } = useAuth();
  const [showBudget, setShowBudget] = useState(false);

  const { data: trip, isLoading: tripLoading } = useTrip(slug);
  const { data: stops } = useStops(slug);
  const { data: budget } = useBudget(slug);

  if (tripLoading) return <div className="flex h-64 items-center justify-center"><Spinner /></div>;
  if (!trip) return <ErrorState message="Trip not found." />;

  const isOwner = user?.id === trip.owner_id;

  return (
    <PageWrapper
      title={trip.title}
      description={trip.description ?? undefined}
      actions={
        isOwner ? (
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              className="gap-2"
              onClick={() => setShowBudget(!showBudget)}
            >
              <DollarSign className="h-4 w-4" />
              {showBudget ? "Timeline" : "Budget"}
            </Button>
            <Link to={`/u/${user?.username}/trips/${slug}/build`}>
              <Button size="sm" className="gap-2">
                <Pencil className="h-4 w-4" /> Edit
              </Button>
            </Link>
          </div>
        ) : null
      }
    >
      {showBudget && budget ? (
        <BudgetChart budget={budget} />
      ) : (
        <TimelineView stops={stops ?? []} />
      )}
    </PageWrapper>
  );
}
