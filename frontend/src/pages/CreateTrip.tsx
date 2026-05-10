import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { tripSchema, type TripFormInput } from "@/schemas/trip.schema";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useCreateTrip } from "@/hooks/useTrips";
import { useAuth } from "@/hooks/useAuth";

export default function CreateTrip() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { mutateAsync, isPending } = useCreateTrip();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TripFormInput>({ resolver: zodResolver(tripSchema) });

  const onSubmit = async (data: TripFormInput) => {
    const trip = await mutateAsync(data);
    navigate(`/u/${user?.username}/trips/${trip.slug}/build`);
  };

  return (
    <PageWrapper title="Create a new trip" description="Set the basics — you can edit everything later.">
      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Trip details</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
            <Input
              label="Trip name *"
              error={errors.title?.message}
              {...register("title")}
              placeholder="e.g. South India Road Trip"
            />
            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="What's this trip about?"
                {...register("description")}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Start date"
                type="date"
                error={errors.start_date?.message}
                {...register("start_date")}
              />
              <Input
                label="End date"
                type="date"
                error={errors.end_date?.message}
                {...register("end_date")}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Budget (USD)"
                type="number"
                min="0"
                error={errors.budget_total_usd?.message}
                {...register("budget_total_usd", { valueAsNumber: true })}
                placeholder="e.g. 2000"
              />
              <Input
                label="Travelers"
                type="number"
                min="1"
                error={errors.traveler_count?.message}
                {...register("traveler_count", { valueAsNumber: true })}
                placeholder="1"
              />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => navigate(-1)}>
                Cancel
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending ? "Creating…" : "Create trip"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </PageWrapper>
  );
}
