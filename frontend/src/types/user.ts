export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  bio: string | null;
  avatar_url: string | null;
  home_city: string | null;
  preferred_currency: string;
  travel_style: string | null;
  languages: string | null;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserUpdateInput {
  full_name?: string;
  bio?: string;
  home_city?: string;
  preferred_currency?: string;
  travel_style?: string;
  languages?: string;
}
