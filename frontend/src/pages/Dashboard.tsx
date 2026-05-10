import { Link } from "react-router-dom";
import { PlusCircle, Map, Clock } from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { TripCard } from "@/components/trip/TripCard";
import { Skeleton } from "@/components/ui/Skeleton";
import { EmptyState } from "@/components/shared/EmptyState";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useAuth } from "@/hooks/useAuth";
import { useTrips } from "@/hooks/useTrips";

export default function Dashboard() {
  const { user } = useAuth();
  const { data, isLoading } = useTrips({ per_page: 4 });

  return (
    <PageWrapper
      title={`Welcome back, ${user?.full_name?.split(" ")[0] ?? user?.username}!`}
      description="Here's an overview of your travel plans."
      actions={
        <Link to={`/u/${user?.username}/trips/new`}>
          <Button className="gap-2">
            <PlusCircle className="h-4 w-4" /> New trip
          </Button>
        </Link>
      }
    >
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Clock className="h-4 w-4" /> Recent trips
          </h2>
          <Link to={`/u/${user?.username}/trips`}>
            <Button variant="ghost" size="sm">View all</Button>
          </Link>
        </div>
        {isLoading ? (
          <div className="grid sm:grid-cols-2 gap-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-48" />
            ))}
          </div>
        ) : data?.items?.length ? (
          <motion.div
            className="grid sm:grid-cols-2 gap-4"
            initial="hidden"
            animate="visible"
            variants={{
              hidden: {},
              visible: { transition: { staggerChildren: 0.07 } },
            }}
          >
            {data.items.map((trip) => (
              <motion.div
                key={trip.id}
                variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}
              >
                <TripCard trip={trip} />
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <EmptyState
            title="No trips yet"
            description="Create your first trip to get started."
            action={
              <Link to={`/u/${user?.username}/trips/new`}>
                <Button>Create a trip</Button>
              </Link>
            }
          />
        )}
      </section>
    </PageWrapper>
  );
}
