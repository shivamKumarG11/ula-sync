import { Heart, MessageCircle, Share2 } from "lucide-react";
import { Card, CardContent, CardFooter } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/utils/dates";
import { useToggleLike } from "@/hooks/useCommunity";
import { useAuthStore } from "@/store/authStore";
import type { CommunityPost } from "@/types/community";

interface CommunityPostCardProps {
  post: CommunityPost;
  onClick?: () => void;
}

export function CommunityPostCard({ post, onClick }: CommunityPostCardProps) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const { mutate: toggleLike } = useToggleLike(post.id);

  return (
    <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={onClick}>
      {post.cover_photo_url && (
        <div className="h-40 overflow-hidden rounded-t-lg">
          <img src={post.cover_photo_url} alt={post.title} className="h-full w-full object-cover" />
        </div>
      )}
      <CardContent className="pt-4">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <h3 className="font-semibold line-clamp-2">{post.title}</h3>
            <p className="text-xs text-muted-foreground mt-1">
              by @{post.author_username} · {formatDate(post.created_at)}
            </p>
          </div>
        </div>
        {post.content && (
          <p className="text-sm text-muted-foreground mt-2 line-clamp-3">{post.content}</p>
        )}
        <div className="flex gap-2 flex-wrap mt-3">
          {post.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              #{tag}
            </Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="gap-4 text-sm text-muted-foreground">
        <Button
          variant="ghost"
          size="sm"
          className={`gap-1 px-2 ${post.is_liked ? "text-red-500" : ""}`}
          onClick={(e) => {
            e.stopPropagation();
            if (isAuthenticated) toggleLike();
          }}
        >
          <Heart className={`h-4 w-4 ${post.is_liked ? "fill-red-500" : ""}`} />
          {post.likes_count}
        </Button>
        <span className="flex items-center gap-1">
          <MessageCircle className="h-4 w-4" />
          {post.comments_count}
        </span>
      </CardFooter>
    </Card>
  );
}
