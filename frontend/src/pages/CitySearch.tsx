import { useState } from "react";
import { MapPin, Globe } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Skeleton } from "@/components/ui/Skeleton";
import { SearchBar } from "@/components/shared/SearchBar";
import { Pagination } from "@/components/shared/Pagination";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useCities } from "@/hooks/useCities";
import { useDebounce } from "@/hooks/useDebounce";
import { formatCurrency } from "@/utils/formatters";
import type { City } from "@/types/city";

function CityCard({ city, onClick }: { city: City; onClick: () => void }) {
  return (
    <Card
      className="cursor-pointer hover:shadow-md transition-shadow overflow-hidden group"
      onClick={onClick}
    >
      {city.cover_photo_url && (
        <div className="h-36 overflow-hidden">
          <img
            src={city.cover_photo_url}
            alt={city.name}
            className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
      )}
      <CardContent className="pt-3 pb-4">
        <h3 className="font-semibold">{city.name}</h3>
        <p className="text-xs text-muted-foreground flex items-center gap-1 mt-0.5">
          <Globe className="h-3 w-3" />
          {city.country}
          {city.region && `, ${city.region}`}
        </p>
        {city.cost_index_usd && (
          <p className="text-xs text-muted-foreground mt-1">
            ~{formatCurrency(city.cost_index_usd)} / trip
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default function CitySearch() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<City | null>(null);
  const debouncedQ = useDebounce(q, 300);

  const { data, isLoading } = useCities({ q: debouncedQ || undefined, page, per_page: 12 });

  return (
    <PageWrapper title="Explore Cities" description="Browse our curated collection of travel destinations.">
      <SearchBar
        value={q}
        onChange={(v) => { setQ(v); setPage(1); }}
        placeholder="Search cities…"
        className="max-w-sm"
      />

      {isLoading ? (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      ) : (
        <>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {data?.items?.map((city) => (
              <CityCard key={city.id} city={city} onClick={() => setSelected(city)} />
            ))}
          </div>
          {data && (
            <Pagination page={data.page} pages={data.pages} onPageChange={setPage} />
          )}
        </>
      )}
    </PageWrapper>
  );
}
