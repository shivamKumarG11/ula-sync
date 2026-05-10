import client from "./client";
import type { User, UserUpdateInput } from "@/types/user";

interface RegisterInput {
  email: string;
  password: string;
  full_name: string;
}

interface LoginInput {
  email: string;
  password: string;
}

export const authApi = {
  register: (data: RegisterInput) =>
    client.post<{ user: User; message: string }>("/api/v1/auth/register", data),

  login: (data: LoginInput) =>
    client.post<{ user: User; message: string }>("/api/v1/auth/login", data),

  refresh: () => client.post("/api/v1/auth/refresh"),

  logout: () => client.post("/api/v1/auth/logout"),

  me: () => client.get<User>("/api/v1/auth/me"),

  updateMe: (data: UserUpdateInput) =>
    client.put<User>("/api/v1/users/me", data),
};
