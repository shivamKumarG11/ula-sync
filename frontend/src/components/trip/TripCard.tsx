import { Link } from "react-router-dom";
import { MapPin, Calendar, Users } from "lucide-react";
import { Card, CardContent, CardFooter } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatDate } from "@/utils/dates";
import type { Trip } from "@/types/trip";

interface TripCardProps {
  trip: Trip;
}

const statusVariant: Record<string, "default" | "success" | "secondary" | "destructive"> = {
  planning: "secondary",
  active: "success",
  completed: "default",
  cancelled: "destructive",
};

export function TripCard({ trip }: TripCardProps) {
  return (
    <Link to={`/u/${trip.owner_id}/trips/${trip.slug}`}>
      <Card className="group overflow-hidden hover:shadow-md transition-shadow cursor-pointer">
        {trip.cover_photo_url && (
          <div className="h-40 overflow-hidden">
            <img
              src={trip.cover_photo_url}
              alt={trip.title}
              className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          </div>
        )}
        <CardContent className="pt-4">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-semibold line-clamp-1">{trip.title}</h3>
            <Badge variant={statusVariant[trip.status]}>{trip.status}</Badge>
          </div>
          {trip.description && (
            <p className="text-sm text-muted-foreground mt-1 line-clamp-2">{trip.description}</p>
          )}
        </CardContent>
        <CardFooter className="gap-4 text-xs text-muted-foreground">
          {(trip.start_date || trip.end_date) && (
            <span className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              {formatDate(trip.start_date)} – {formatDate(trip.end_date)}
            </span>
          )}
          {trip.traveler_count > 1 && (
            <span className="flex items-center gap-1">
              <Users className="h-3 w-3" />
              {trip.traveler_count}
            </span>
          )}
        </CardFooter>
      </Card>
    </Link>
  );
}
