import { StopCard } from "@/components/trip/StopCard";
import type { Stop } from "@/types/stop";

interface TimelineViewProps {
  stops: Stop[];
  onStopClick?: (stop: Stop) => void;
}

export function TimelineView({ stops, onStopClick }: TimelineViewProps) {
  if (stops.length === 0) {
    return (
      <p className="text-sm text-muted-foreground text-center py-8">
        No stops added yet. Start building your itinerary!
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {stops.map((stop, i) => (
        <StopCard
          key={stop.id}
          stop={stop}
          index={i}
          onClick={() => onStopClick?.(stop)}
        />
      ))}
    </div>
  );
}
