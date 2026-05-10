import { cn } from "@/utils/cn";
import type { ReactNode } from "react";

interface PageWrapperProps {
  title?: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function PageWrapper({ title, description, actions, children, className }: PageWrapperProps) {
  return (
    <div className={cn("flex flex-col gap-6", className)}>
      {(title || actions) && (
        <div className="flex items-start justify-between gap-4">
          <div>
            {title && <h1 className="text-2xl font-bold tracking-tight">{title}</h1>}
            {description && (
              <p className="text-muted-foreground mt-1 text-sm">{description}</p>
            )}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </div>
      )}
      {children}
    </div>
  );
}
