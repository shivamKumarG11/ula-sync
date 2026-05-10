import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Map,
  PlusCircle,
  Compass,
  Users,
  Settings,
  X,
} from "lucide-react";
import { cn } from "@/utils/cn";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { useUIStore } from "@/store/uiStore";

const navItems = (username: string) => [
  { to: `/u/${username}/dashboard`, label: "Dashboard", icon: LayoutDashboard },
  { to: `/u/${username}/trips`, label: "My Trips", icon: Map },
  { to: `/u/${username}/trips/new`, label: "New Trip", icon: PlusCircle },
  { to: "/cities", label: "Explore Cities", icon: Compass },
  { to: "/community", label: "Community", icon: Users },
  { to: `/u/${username}/profile`, label: "Settings", icon: Settings },
];

export function Sidebar() {
  const { user } = useAuth();
  const { sidebarOpen, setSidebarOpen } = useUIStore();

  if (!user) return null;

  return (
    <>
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      <aside
        className={cn(
          "fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 border-r bg-background transition-transform duration-200 md:static md:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-full flex-col gap-1 p-4">
          <Button
            variant="ghost"
            size="icon"
            className="self-end md:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
          {navItems(user.username).map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                )
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </div>
      </aside>
    </>
  );
}
