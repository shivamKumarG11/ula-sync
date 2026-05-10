import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authApi } from "@/api/auth";
import { useAuthStore } from "@/store/authStore";
import type { LoginInput, RegisterInput } from "@/schemas/auth.schema";
import type { UserUpdateInput } from "@/types/user";

export function useAuth() {
  const { user, isAuthenticated, setUser, logout: clearUser } = useAuthStore();
  const qc = useQueryClient();

  const meQuery = useQuery({
    queryKey: ["me"],
    queryFn: () => authApi.me().then((r) => r.data),
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  });

  const loginMutation = useMutation({
    mutationFn: (data: LoginInput) => authApi.login(data).then((r) => r.data),
    onSuccess: (data) => setUser(data.user),
  });

  const registerMutation = useMutation({
    mutationFn: (data: RegisterInput) =>
      authApi.register({ email: data.email, password: data.password, full_name: data.full_name })
        .then((r) => r.data),
    onSuccess: (data) => setUser(data.user),
  });

  const logoutMutation = useMutation({
    mutationFn: () => authApi.logout(),
    onSuccess: () => clearUser(),
  });

  const updateProfileMutation = useMutation({
    mutationFn: (data: UserUpdateInput) => authApi.updateMe(data).then((r) => r.data),
    onSuccess: (data) => {
      setUser(data);
      qc.invalidateQueries({ queryKey: ["me"] });
    },
  });

  return {
    user: meQuery.data ?? user,
    isAuthenticated,
    isLoadingMe: meQuery.isLoading,
    login: loginMutation.mutateAsync,
    isLoginPending: loginMutation.isPending,
    register: registerMutation.mutateAsync,
    isRegisterPending: registerMutation.isPending,
    logout: logoutMutation.mutate,
    updateProfile: updateProfileMutation.mutateAsync,
    isUpdatingProfile: updateProfileMutation.isPending,
  };
}
