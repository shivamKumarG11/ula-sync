import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { communityApi } from "@/api/community";
import type { CommunityPostCreateInput, CommunityCommentCreateInput } from "@/types/community";

export function useCommunityPosts(params?: {
  page?: number;
  per_page?: number;
  tag?: string;
  q?: string;
}) {
  return useQuery({
    queryKey: ["community-posts", params],
    queryFn: () => communityApi.list(params).then((r) => r.data),
  });
}

export function useCommunityPost(postId: number) {
  return useQuery({
    queryKey: ["community-post", postId],
    queryFn: () => communityApi.get(postId).then((r) => r.data),
    enabled: !!postId,
  });
}

export function useCreatePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CommunityPostCreateInput) =>
      communityApi.create(data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["community-posts"] }),
  });
}

export function useToggleLike(postId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => communityApi.toggleLike(postId).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["community-post", postId] });
      qc.invalidateQueries({ queryKey: ["community-posts"] });
    },
  });
}

export function useComments(postId: number) {
  return useQuery({
    queryKey: ["comments", postId],
    queryFn: () => communityApi.listComments(postId).then((r) => r.data),
    enabled: !!postId,
  });
}

export function useAddComment(postId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CommunityCommentCreateInput) =>
      communityApi.addComment(postId, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["comments", postId] }),
  });
}

export function useDeleteComment(postId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (commentId: number) => communityApi.deleteComment(postId, commentId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["comments", postId] }),
  });
}
