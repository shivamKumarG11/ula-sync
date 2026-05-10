import { Clock, DollarSign, MapPin } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDuration, formatCurrency } from "@/utils/formatters";
import type { Activity } from "@/types/activity";

interface ActivityCardProps {
  activity: Activity;
  onAdd?: () => void;
  added?: boolean;
}

export function ActivityCard({ activity, onAdd, added }: ActivityCardProps) {
  return (
    <Card className="hover:shadow-sm transition-shadow">
      <CardContent className="pt-4 flex flex-col gap-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <h4 className="font-medium text-sm">{activity.name}</h4>
            {activity.description && (
              <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                {activity.description}
              </p>
            )}
          </div>
          <Badge variant="secondary" className="capitalize text-xs shrink-0">
            {activity.category}
          </Badge>
        </div>
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          {activity.duration_hours && (
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {formatDuration(activity.duration_hours)}
            </span>
          )}
          <span className="flex items-center gap-1">
            <DollarSign className="h-3 w-3" />
            {activity.cost_usd > 0 ? formatCurrency(activity.cost_usd) : "Free"}
          </span>
          {activity.map_link && (
            <a
              href={activity.map_link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-primary hover:underline"
            >
              <MapPin className="h-3 w-3" />
              Map
            </a>
          )}
        </div>
        {onAdd && (
          <Button
            size="sm"
            variant={added ? "secondary" : "default"}
            onClick={onAdd}
            disabled={added}
            className="w-full mt-1"
          >
            {added ? "Added" : "Add to stop"}
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
