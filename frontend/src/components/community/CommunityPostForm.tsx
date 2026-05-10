import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { communityPostSchema, type CommunityPostFormInput } from "@/schemas/community.schema";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useCreatePost } from "@/hooks/useCommunity";

interface CommunityPostFormProps {
  onSuccess?: () => void;
}

export function CommunityPostForm({ onSuccess }: CommunityPostFormProps) {
  const { mutateAsync, isPending } = useCreatePost();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CommunityPostFormInput>({
    resolver: zodResolver(communityPostSchema),
  });

  const onSubmit = async (data: CommunityPostFormInput) => {
    await mutateAsync(data);
    reset();
    onSuccess?.();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
      <Input
        label="Title"
        error={errors.title?.message}
        {...register("title")}
        placeholder="Your post title"
      />
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium">Content</label>
        <textarea
          className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          placeholder="Share your travel story, tips, or experience…"
          {...register("content")}
        />
        {errors.content && <p className="text-xs text-destructive">{errors.content.message}</p>}
      </div>
      <Button type="submit" disabled={isPending}>
        {isPending ? "Publishing…" : "Publish post"}
      </Button>
    </form>
  );
}
