export interface CommunityPost {
  id: number;
  user_id: number;
  author_username: string;
  author_avatar: string | null;
  trip_id: number | null;
  title: string;
  content: string;
  tags: string[];
  cover_photo_url: string | null;
  likes_count: number;
  comments_count: number;
  is_liked: boolean;
  created_at: string;
  updated_at: string;
}

export interface CommunityComment {
  id: number;
  post_id: number;
  user_id: number;
  author_username: string;
  author_avatar: string | null;
  content: string;
  created_at: string;
}

export interface CommunityPostCreateInput {
  title: string;
  content: string;
  tags?: string[];
  trip_id?: number;
}

export interface CommunityCommentCreateInput {
  content: string;
}
