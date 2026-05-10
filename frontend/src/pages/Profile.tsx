import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { MapPin, Trash2 } from "lucide-react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useAuth } from "@/hooks/useAuth";
import { useSavedCities, useUnsaveCity } from "@/hooks/useCities";
import { formatCurrency } from "@/utils/formatters";
import toast from "react-hot-toast";

const profileSchema = z.object({
  full_name: z.string().min(1, "Name is required").max(80),
  email: z.string().email(),
  avatar_url: z.string().url("Invalid URL").optional().or(z.literal("")),
  preferred_currency: z.string().length(3).toUpperCase().optional(),
  home_city: z.string().max(60).optional(),
  bio: z.string().max(300).optional(),
});

type ProfileFormInput = z.infer<typeof profileSchema>;

export default function Profile() {
  const { user, updateProfile, isUpdatingProfile } = useAuth();
  const { data: savedCities, isLoading: citiesLoading } = useSavedCities();
  const { mutate: unsave } = useUnsaveCity();

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<ProfileFormInput>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      full_name: user?.full_name ?? "",
      email: user?.email ?? "",
      avatar_url: user?.avatar_url ?? "",
      preferred_currency: user?.preferred_currency ?? "USD",
      home_city: user?.home_city ?? "",
      bio: user?.bio ?? "",
    },
  });

  const onSubmit = async (data: ProfileFormInput) => {
    try {
      await updateProfile(data);
      toast.success("Profile updated");
    } catch {
      toast.error("Failed to update profile");
    }
  };

  return (
    <PageWrapper title="Profile" description="Manage your account settings and preferences.">
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <Card>
            <CardContent className="pt-6">
              <h2 className="font-semibold text-lg mb-4">Account Details</h2>
              <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
                <div className="grid sm:grid-cols-2 gap-4">
                  <Input
                    label="Full Name"
                    error={errors.full_name?.message}
                    {...register("full_name")}
                  />
                  <Input
                    label="Email"
                    type="email"
                    error={errors.email?.message}
                    {...register("email")}
                  />
                </div>
                <Input
                  label="Avatar URL"
                  placeholder="https://…"
                  error={errors.avatar_url?.message}
                  {...register("avatar_url")}
                />
                <div className="grid sm:grid-cols-2 gap-4">
                  <Input
                    label="Home City"
                    placeholder="e.g. New York"
                    error={errors.home_city?.message}
                    {...register("home_city")}
                  />
                  <Input
                    label="Preferred Currency"
                    placeholder="USD"
                    error={errors.preferred_currency?.message}
                    {...register("preferred_currency")}
                  />
                </div>
                <div className="flex flex-col gap-1">
                  <label className="text-sm font-medium">Bio</label>
                  <textarea
                    className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Tell the community about yourself…"
                    {...register("bio")}
                  />
                  {errors.bio && <p className="text-xs text-destructive">{errors.bio.message}</p>}
                </div>
                <Button type="submit" disabled={!isDirty || isUpdatingProfile} className="self-start">
                  {isUpdatingProfile ? "Saving…" : "Save Changes"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        <div className="flex flex-col gap-4">
          {user?.avatar_url && (
            <Card>
              <CardContent className="pt-6 flex flex-col items-center gap-3">
                <img
                  src={user.avatar_url}
                  alt={user.full_name}
                  className="h-20 w-20 rounded-full object-cover border-2 border-border"
                />
                <div className="text-center">
                  <p className="font-semibold">{user.full_name}</p>
                  <p className="text-xs text-muted-foreground">@{user.username}</p>
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardContent className="pt-6">
              <h2 className="font-semibold mb-3">Saved Cities</h2>
              {citiesLoading ? (
                <div className="flex flex-col gap-2">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <Skeleton key={i} className="h-10" />
                  ))}
                </div>
              ) : !savedCities?.length ? (
                <p className="text-sm text-muted-foreground">No saved cities yet.</p>
              ) : (
                <ul className="flex flex-col gap-2">
                  {savedCities.map((sc) => (
                    <motion.li
                      key={sc.id}
                      layout
                      className="flex items-center justify-between text-sm"
                    >
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3 w-3 text-muted-foreground" />
                        {sc.city.name}
                        {sc.city.cost_index_usd && (
                          <span className="text-xs text-muted-foreground ml-1">
                            ~{formatCurrency(sc.city.cost_index_usd)}
                          </span>
                        )}
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                        onClick={() => unsave(sc.city_id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </motion.li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageWrapper>
  );
}
