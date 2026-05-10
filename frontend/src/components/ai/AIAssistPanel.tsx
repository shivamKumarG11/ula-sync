import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import type { ReactNode } from "react";

interface AIAssistPanelProps {
  title?: string;
  description?: string;
  onGenerate: () => void;
  isLoading?: boolean;
  children?: ReactNode;
}

export function AIAssistPanel({
  title = "AI Assistant",
  description,
  onGenerate,
  isLoading,
  children,
}: AIAssistPanelProps) {
  return (
    <div className="rounded-xl border bg-gradient-to-br from-primary/5 to-primary/10 p-4 flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-primary" />
        <span className="text-sm font-semibold">{title}</span>
      </div>
      {description && (
        <p className="text-xs text-muted-foreground">{description}</p>
      )}
      {children}
      <Button
        size="sm"
        className="gap-2"
        onClick={onGenerate}
        disabled={isLoading}
      >
        {isLoading ? <Spinner size="sm" /> : <Sparkles className="h-3 w-3" />}
        {isLoading ? "Generating…" : "Generate"}
      </Button>
    </div>
  );
}
