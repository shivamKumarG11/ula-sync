import { Star, ThumbsUp, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import type { AIFeedbackResponse } from "@/types/ai";

interface AIFeedbackPanelProps {
  feedback: AIFeedbackResponse;
}

export function AIFeedbackPanel({ feedback }: AIFeedbackPanelProps) {
  return (
    <Card>
      <CardContent className="pt-4 flex flex-col gap-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star
                key={i}
                className={`h-5 w-5 ${i < Math.round(feedback.score / 2) ? "text-yellow-400 fill-yellow-400" : "text-muted-foreground"}`}
              />
            ))}
          </div>
          <Badge variant="secondary">{feedback.score}/10</Badge>
        </div>
        <p className="text-sm">{feedback.summary}</p>
        {feedback.strengths.length > 0 && (
          <div>
            <p className="text-xs font-semibold text-green-600 flex items-center gap-1 mb-1">
              <ThumbsUp className="h-3 w-3" /> Strengths
            </p>
            <ul className="text-xs text-muted-foreground space-y-1">
              {feedback.strengths.map((s, i) => (
                <li key={i}>• {s}</li>
              ))}
            </ul>
          </div>
        )}
        {feedback.improvements.length > 0 && (
          <div>
            <p className="text-xs font-semibold text-orange-500 flex items-center gap-1 mb-1">
              <AlertCircle className="h-3 w-3" /> Improvements
            </p>
            <ul className="text-xs text-muted-foreground space-y-1">
              {feedback.improvements.map((s, i) => (
                <li key={i}>• {s}</li>
              ))}
            </ul>
          </div>
        )}
        {feedback.seasonal_notes && (
          <p className="text-xs text-muted-foreground italic">{feedback.seasonal_notes}</p>
        )}
      </CardContent>
    </Card>
  );
}
