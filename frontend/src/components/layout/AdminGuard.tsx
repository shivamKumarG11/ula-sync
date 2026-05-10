import { Navigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import type { ReactNode } from "react";

interface AdminGuardProps {
  children: ReactNode;
}

export function AdminGuard({ children }: AdminGuardProps) {
  const user = useAuthStore((s) => s.user);
  if (!user?.is_admin) return <Navigate to="/" replace />;
  return <>{children}</>;
}
