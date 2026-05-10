import { MapPin, Calendar, Moon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatDate } from "@/utils/dates";
import type { Stop } from "@/types/stop";

interface StopCardProps {
  stop: Stop;
  index: number;
  onClick?: () => void;
}

export function StopCard({ stop, index, onClick }: StopCardProps) {
  return (
    <Card
      className="group cursor-pointer hover:shadow-md transition-shadow"
      onClick={onClick}
    >
      <CardContent className="flex gap-4 pt-4">
        <div className="flex flex-col items-center gap-1">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
            {index + 1}
          </div>
          <div className="flex-1 w-px bg-border" />
        </div>
        <div className="flex-1 pb-4">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-semibold">{stop.city_name}</h3>
            <Badge variant="outline" className="text-xs">
              {stop.city_country}
            </Badge>
          </div>
          <div className="flex gap-4 mt-2 text-xs text-muted-foreground flex-wrap">
            {(stop.arrival_date || stop.departure_date) && (
              <span className="flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {formatDate(stop.arrival_date)} – {formatDate(stop.departure_date)}
              </span>
            )}
            {stop.nights && (
              <span className="flex items-center gap-1">
                <Moon className="h-3 w-3" />
                {stop.nights} nights
              </span>
            )}
            {stop.accommodation_name && (
              <span className="flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                {stop.accommodation_name}
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
