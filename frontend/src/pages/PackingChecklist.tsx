import { useState } from "react";
import { useParams } from "react-router-dom";
import { Plus, RotateCcw, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import { Skeleton } from "@/components/ui/Skeleton";
import { EmptyState } from "@/components/shared/EmptyState";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { usePacking, useTogglePacked, useSeedPacking } from "@/hooks/usePacking";
import { cn } from "@/utils/cn";
import type { PackingCategory } from "@/types/packing";

const CATEGORY_COLORS: Record<PackingCategory, string> = {
  clothing: "bg-blue-100 text-blue-700",
  toiletries: "bg-pink-100 text-pink-700",
  electronics: "bg-purple-100 text-purple-700",
  documents: "bg-yellow-100 text-yellow-700",
  health: "bg-green-100 text-green-700",
  accessories: "bg-orange-100 text-orange-700",
  other: "bg-gray-100 text-gray-700",
};

export default function PackingChecklist() {
  const { tripSlug } = useParams<{ tripSlug: string }>();
  const slug = tripSlug!;
  const { data: items, isLoading } = usePacking(slug);
  const { mutate: togglePacked } = useTogglePacked(slug);
  const { mutate: seedItems, isPending: seeding } = useSeedPacking(slug);
  const [filter, setFilter] = useState<PackingCategory | "all">("all");

  const packed = items?.filter((i) => i.is_packed).length ?? 0;
  const total = items?.length ?? 0;
  const progress = total > 0 ? Math.round((packed / total) * 100) : 0;

  const filtered =
    filter === "all" ? items : items?.filter((i) => i.category === filter);

  return (
    <PageWrapper
      title="Packing checklist"
      description={`${packed} of ${total} items packed`}
      actions={
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => seedItems()}
            disabled={seeding}
          >
            <Sparkles className="h-4 w-4" />
            {seeding ? "Seeding…" : "AI seed"}
          </Button>
          <Button size="sm" className="gap-2">
            <Plus className="h-4 w-4" /> Add item
          </Button>
        </div>
      }
    >
      <div className="h-2 w-full rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      {isLoading ? (
        <div className="flex flex-col gap-3">
          {Array.from({ length: 8 }).map((_, i) => <Skeleton key={i} className="h-12" />)}
        </div>
      ) : !items?.length ? (
        <EmptyState
          title="No items yet"
          description="Add items manually or use AI to seed a checklist based on your destinations."
        />
      ) : (
        <div className="flex flex-col gap-3">
          {filtered?.map((item) => (
            <div
              key={item.id}
              className={cn(
                "flex items-center gap-3 rounded-lg border p-3 transition-opacity",
                item.is_packed && "opacity-60",
              )}
            >
              <input
                type="checkbox"
                checked={item.is_packed}
                onChange={() => togglePacked({ itemId: item.id, is_packed: !item.is_packed })}
                className="h-4 w-4 rounded border-input"
              />
              <span className={cn("flex-1 text-sm", item.is_packed && "line-through")}>
                {item.quantity > 1 && (
                  <span className="text-muted-foreground mr-1">{item.quantity}×</span>
                )}
                {item.name}
                {item.is_essential && (
                  <span className="ml-2 text-xs text-red-500 font-medium">essential</span>
                )}
              </span>
              <span
                className={cn(
                  "rounded-full px-2 py-0.5 text-xs font-medium capitalize",
                  CATEGORY_COLORS[item.category],
                )}
              >
                {item.category}
              </span>
            </div>
          ))}
        </div>
      )}
    </PageWrapper>
  );
}
