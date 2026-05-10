import { Sun, Cloud, Droplets, Wind } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Skeleton } from "@/components/ui/Skeleton";

interface WeatherData {
  temp_c?: number;
  description?: string;
  humidity?: number;
  wind_kmh?: number;
}

interface WeatherWidgetProps {
  weather?: WeatherData;
  isLoading?: boolean;
  cityName?: string;
}

export function WeatherWidget({ weather, isLoading, cityName }: WeatherWidgetProps) {
  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-4 flex flex-col gap-2">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-8 w-16" />
          <Skeleton className="h-3 w-32" />
        </CardContent>
      </Card>
    );
  }

  if (!weather) return null;

  return (
    <Card>
      <CardContent className="pt-4">
        <p className="text-xs text-muted-foreground">{cityName} · Now</p>
        <div className="flex items-center gap-3 mt-2">
          <Sun className="h-8 w-8 text-yellow-400" />
          <div>
            <p className="text-2xl font-bold">{weather.temp_c?.toFixed(0)}°C</p>
            <p className="text-xs text-muted-foreground capitalize">{weather.description}</p>
          </div>
        </div>
        <div className="flex gap-4 mt-3 text-xs text-muted-foreground">
          {weather.humidity !== undefined && (
            <span className="flex items-center gap-1">
              <Droplets className="h-3 w-3" /> {weather.humidity}%
            </span>
          )}
          {weather.wind_kmh !== undefined && (
            <span className="flex items-center gap-1">
              <Wind className="h-3 w-3" /> {weather.wind_kmh} km/h
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
