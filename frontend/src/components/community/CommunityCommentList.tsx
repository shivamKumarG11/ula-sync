import { useState } from "react";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { formatDate } from "@/utils/dates";
import { useComments, useAddComment, useDeleteComment } from "@/hooks/useCommunity";
import { useAuthStore } from "@/store/authStore";

interface CommunityCommentListProps {
  postId: number;
}

export function CommunityCommentList({ postId }: CommunityCommentListProps) {
  const { data: comments, isLoading } = useComments(postId);
  const { mutateAsync: addComment, isPending } = useAddComment(postId);
  const { mutate: deleteComment } = useDeleteComment(postId);
  const user = useAuthStore((s) => s.user);
  const [text, setText] = useState("");

  const handleAdd = async () => {
    if (!text.trim()) return;
    await addComment({ content: text });
    setText("");
  };

  if (isLoading) return <Spinner />;

  return (
    <div className="flex flex-col gap-4">
      {comments?.map((c) => (
        <div key={c.id} className="flex gap-3">
          <div className="flex-1">
            <p className="text-xs font-medium">
              @{c.author_username}{" "}
              <span className="text-muted-foreground font-normal">{formatDate(c.created_at)}</span>
            </p>
            <p className="text-sm mt-0.5">{c.content}</p>
          </div>
          {user?.username === c.author_username && (
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-muted-foreground hover:text-destructive"
              onClick={() => deleteComment(c.id)}
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          )}
        </div>
      ))}
      {user && (
        <div className="flex gap-2 mt-2">
          <Input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write a comment…"
            className="h-9 flex-1"
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
          />
          <Button size="sm" className="h-9" disabled={isPending} onClick={handleAdd}>
            Post
          </Button>
        </div>
      )}
    </div>
  );
}
