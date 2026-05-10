import { useState } from "react";
import { useParams } from "react-router-dom";
import { DragDropContext, Droppable, Draggable, type DropResult } from "@hello-pangea/dnd";
import { GripVertical, Plus, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/shared/ErrorState";
import { EmptyState } from "@/components/shared/EmptyState";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { AIAssistPanel } from "@/components/ai/AIAssistPanel";
import { useTrip } from "@/hooks/useTrips";
import { useStops, useReorderStops } from "@/hooks/useStops";
import { useGenerateItinerary } from "@/hooks/useAI";

export default function ItineraryBuilder() {
  const { tripSlug } = useParams<{ tripSlug: string }>();
  const slug = tripSlug!;

  const { data: trip, isLoading: tripLoading } = useTrip(slug);
  const { data: stops, isLoading: stopsLoading } = useStops(slug);
  const { mutate: reorder } = useReorderStops(slug);
  const { mutateAsync: generateItinerary, isPending: aiPending } = useGenerateItinerary(slug);
  const [aiResult, setAiResult] = useState<string | null>(null);

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination || !stops) return;
    const reordered = Array.from(stops);
    const [moved] = reordered.splice(result.source.index, 1);
    reordered.splice(result.destination.index, 0, moved);
    reorder({ ordered_ids: reordered.map((s) => s.id) });
  };

  if (tripLoading) return <div className="flex h-64 items-center justify-center"><Spinner /></div>;
  if (!trip) return <ErrorState message="Trip not found." />;

  return (
    <PageWrapper
      title={trip.title}
      description="Drag stops to reorder, add cities, and let AI plan your days."
      actions={
        <Button size="sm" className="gap-2">
          <Plus className="h-4 w-4" /> Add stop
        </Button>
      }
    >
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {stopsLoading ? (
            <Spinner />
          ) : !stops?.length ? (
            <EmptyState
              title="No stops yet"
              description="Add cities to build your itinerary."
            />
          ) : (
            <DragDropContext onDragEnd={handleDragEnd}>
              <Droppable droppableId="stops">
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className="flex flex-col gap-3"
                  >
                    {stops.map((stop, index) => (
                      <Draggable key={stop.id} draggableId={String(stop.id)} index={index}>
                        {(drag) => (
                          <div
                            ref={drag.innerRef}
                            {...drag.draggableProps}
                            className="flex items-center gap-3 rounded-lg border bg-background p-4 shadow-sm"
                          >
                            <div {...drag.handleProps} className="cursor-grab text-muted-foreground">
                              <GripVertical className="h-5 w-5" />
                            </div>
                            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                              {index + 1}
                            </div>
                            <div className="flex-1">
                              <p className="font-medium">{stop.city_name}</p>
                              <p className="text-xs text-muted-foreground">{stop.city_country}</p>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          )}
        </div>

        <div className="flex flex-col gap-4">
          <AIAssistPanel
            title="AI Itinerary Generator"
            description="Let AI create a complete day-by-day plan for this trip."
            isLoading={aiPending}
            onGenerate={async () => {
              const res = await generateItinerary({});
              setAiResult(res.summary);
            }}
          />
          {aiResult && (
            <div className="rounded-lg border bg-muted/30 p-4 text-sm text-muted-foreground">
              {aiResult}
            </div>
          )}
        </div>
      </div>
    </PageWrapper>
  );
}
