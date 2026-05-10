import { cn } from "@/utils/cn";

interface DividerProps {
  className?: string;
  label?: string;
}

export function Divider({ className, label }: DividerProps) {
  if (label) {
    return (
      <div className={cn("flex items-center gap-3", className)}>
        <div className="flex-1 border-t border-border" />
        <span className="text-xs text-muted-foreground">{label}</span>
        <div className="flex-1 border-t border-border" />
      </div>
    );
  }
  return <hr className={cn("border-border", className)} />;
}
