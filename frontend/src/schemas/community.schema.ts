import { z } from "zod";

export const communityPostSchema = z.object({
  title: z.string().min(5, "Title must be at least 5 characters").max(200),
  content: z.string().min(20, "Content must be at least 20 characters"),
  tags: z.array(z.string().max(30)).max(5).default([]),
  trip_id: z.number().int().positive().optional(),
});

export const communityCommentSchema = z.object({
  content: z.string().min(1, "Comment cannot be empty").max(1000),
});

export type CommunityPostFormInput = z.infer<typeof communityPostSchema>;
export type CommunityCommentFormInput = z.infer<typeof communityCommentSchema>;
