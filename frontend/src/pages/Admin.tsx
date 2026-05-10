import { NavLink, Outlet } from "react-router-dom";
import { Users, MapPin, BarChart2 } from "lucide-react";
import { PageWrapper } from "@/components/layout/PageWrapper";

const adminLinks = [
  { to: "/admin/users", label: "Users", icon: Users },
  { to: "/admin/cities", label: "Cities", icon: MapPin },
  { to: "/admin/analytics", label: "Analytics", icon: BarChart2 },
];

export default function Admin() {
  return (
    <PageWrapper title="Admin" description="Platform management and analytics.">
      <div className="flex gap-2 border-b mb-6">
        {adminLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-1.5 px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                isActive
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </div>
      <Outlet />
    </PageWrapper>
  );
}
