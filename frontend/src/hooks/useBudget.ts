import { useQuery } from "@tanstack/react-query";
import { budgetApi } from "@/api/budget";

export function useBudget(tripSlug: string) {
  return useQuery({
    queryKey: ["budget", tripSlug],
    queryFn: () => budgetApi.get(tripSlug).then((r) => r.data),
    enabled: !!tripSlug,
  });
}
