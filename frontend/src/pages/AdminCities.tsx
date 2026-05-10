import { useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { SearchBar } from "@/components/shared/SearchBar";
import { Pagination } from "@/components/shared/Pagination";
import { EmptyState } from "@/components/shared/EmptyState";
import { ConfirmDialog } from "@/components/shared/ConfirmDialog";
import { useCities } from "@/hooks/useCities";
import { useDebounce } from "@/hooks/useDebounce";
import { formatCurrency } from "@/utils/formatters";
import type { City } from "@/types/city";

export default function AdminCities() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [deleteTarget, setDeleteTarget] = useState<City | null>(null);
  const debouncedQ = useDebounce(q, 300);

  const { data, isLoading } = useCities({ q: debouncedQ || undefined, page, per_page: 15 });

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <SearchBar
          value={q}
          onChange={(v) => { setQ(v); setPage(1); }}
          placeholder="Search cities…"
          className="max-w-sm"
        />
        <Button size="sm">
          <Plus className="h-4 w-4 mr-1" />
          Add City
        </Button>
      </div>

      {isLoading ? (
        <div className="flex flex-col gap-2">
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} className="h-14" />
          ))}
        </div>
      ) : !data?.items?.length ? (
        <EmptyState title="No cities found" />
      ) : (
        <>
          <Card>
            <CardContent className="p-0">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-muted-foreground">
                    <th className="px-4 py-2 font-medium">City</th>
                    <th className="px-4 py-2 font-medium">Country</th>
                    <th className="px-4 py-2 font-medium">Region</th>
                    <th className="px-4 py-2 font-medium">Cost Index</th>
                    <th className="px-4 py-2 font-medium" />
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((city) => (
                    <tr key={city.id} className="border-b last:border-0 hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">
                        <div className="flex items-center gap-2">
                          {city.cover_photo_url && (
                            <img
                              src={city.cover_photo_url}
                              alt={city.name}
                              className="h-7 w-10 rounded object-cover"
                            />
                          )}
                          {city.name}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">{city.country}</td>
                      <td className="px-4 py-3 text-muted-foreground">{city.region ?? "—"}</td>
                      <td className="px-4 py-3">
                        {city.cost_index_usd ? formatCurrency(city.cost_index_usd) : "—"}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex items-center justify-end gap-1">
                          <Button variant="ghost" size="sm">
                            <Pencil className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-destructive hover:text-destructive"
                            onClick={() => setDeleteTarget(city)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
          <Pagination page={data.page} pages={data.pages} onPageChange={setPage} />
        </>
      )}

      <ConfirmDialog
        open={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => setDeleteTarget(null)}
        title={`Delete ${deleteTarget?.name}?`}
        description="This will permanently remove the city and all associated data."
        confirmLabel="Delete"
        destructive
      />
    </div>
  );
}
