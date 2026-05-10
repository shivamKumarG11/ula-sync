import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({
  title = "Nothing here yet",
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16 text-center">
      <Inbox className="h-12 w-12 text-muted-foreground/40" />
      <div>
        <p className="font-medium text-muted-foreground">{title}</p>
        {description && (
          <p className="text-sm text-muted-foreground/70 mt-1">{description}</p>
        )}
      </div>
      {action}
    </div>
  );
}
