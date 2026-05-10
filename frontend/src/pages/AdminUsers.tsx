import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Shield, ShieldOff } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import { SearchBar } from "@/components/shared/SearchBar";
import { Pagination } from "@/components/shared/Pagination";
import { EmptyState } from "@/components/shared/EmptyState";
import { useDebounce } from "@/hooks/useDebounce";
import { formatDate } from "@/utils/dates";
import client from "@/api/client";
import type { PaginatedResponse } from "@/types/api";
import type { User } from "@/types/user";

export default function AdminUsers() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const debouncedQ = useDebounce(q, 300);

  const { data, isLoading } = useQuery({
    queryKey: ["admin-users", debouncedQ, page],
    queryFn: () =>
      client
        .get<PaginatedResponse<User>>("/api/v1/admin/users", {
          params: { q: debouncedQ || undefined, page, per_page: 15 },
        })
        .then((r) => r.data),
  });

  return (
    <div className="flex flex-col gap-4">
      <SearchBar
        value={q}
        onChange={(v) => { setQ(v); setPage(1); }}
        placeholder="Search users…"
        className="max-w-sm"
      />

      {isLoading ? (
        <div className="flex flex-col gap-2">
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} className="h-14" />
          ))}
        </div>
      ) : !data?.items?.length ? (
        <EmptyState title="No users found" />
      ) : (
        <>
          <Card>
            <CardContent className="pt-4 p-0">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-muted-foreground">
                    <th className="px-4 py-2 font-medium">User</th>
                    <th className="px-4 py-2 font-medium">Email</th>
                    <th className="px-4 py-2 font-medium">Joined</th>
                    <th className="px-4 py-2 font-medium">Role</th>
                    <th className="px-4 py-2 font-medium" />
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((user) => (
                    <tr key={user.id} className="border-b last:border-0 hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">
                        <div className="flex items-center gap-2">
                          {user.avatar_url ? (
                            <img
                              src={user.avatar_url}
                              alt={user.full_name ?? user.username}
                              className="h-7 w-7 rounded-full object-cover"
                            />
                          ) : (
                            <div className="h-7 w-7 rounded-full bg-muted flex items-center justify-center text-xs">
                              {(user.full_name ?? user.username).charAt(0).toUpperCase()}
                            </div>
                          )}
                          <span>{user.full_name ?? user.username}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">{user.email}</td>
                      <td className="px-4 py-3 text-muted-foreground">{formatDate(user.created_at)}</td>
                      <td className="px-4 py-3">
                        {user.is_admin ? (
                          <Badge variant="default" className="text-xs">Admin</Badge>
                        ) : (
                          <Badge variant="secondary" className="text-xs">User</Badge>
                        )}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Button variant="ghost" size="sm">
                          {user.is_admin ? (
                            <ShieldOff className="h-4 w-4" />
                          ) : (
                            <Shield className="h-4 w-4" />
                          )}
                        </Button>
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
    </div>
  );
}
