import client from "./client";
import type {
  CommunityPost,
  CommunityComment,
  CommunityPostCreateInput,
  CommunityCommentCreateInput,
} from "@/types/community";
import type { PaginatedResponse } from "@/types/api";

export const communityApi = {
  list: (params?: { page?: number; per_page?: number; tag?: string; q?: string }) =>
    client.get<PaginatedResponse<CommunityPost>>("/api/v1/community", { params }),

  get: (postId: number) => client.get<CommunityPost>(`/api/v1/community/${postId}`),

  create: (data: CommunityPostCreateInput) =>
    client.post<CommunityPost>("/api/v1/community", data),

  update: (postId: number, data: Partial<CommunityPostCreateInput>) =>
    client.put<CommunityPost>(`/api/v1/community/${postId}`, data),

  delete: (postId: number) => client.delete(`/api/v1/community/${postId}`),

  toggleLike: (postId: number) =>
    client.post<{ liked: boolean; likes_count: number }>(
      `/api/v1/community/${postId}/like`,
    ),

  listComments: (postId: number) =>
    client.get<CommunityComment[]>(`/api/v1/community/${postId}/comments`),

  addComment: (postId: number, data: CommunityCommentCreateInput) =>
    client.post<CommunityComment>(`/api/v1/community/${postId}/comments`, data),

  deleteComment: (postId: number, commentId: number) =>
    client.delete(`/api/v1/community/${postId}/comments/${commentId}`),
};
