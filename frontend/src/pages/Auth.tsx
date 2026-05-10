import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Globe } from "lucide-react";
import {
  loginSchema,
  registerSchema,
  type LoginInput,
  type RegisterInput,
} from "@/schemas/auth.schema";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Divider } from "@/components/ui/Divider";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { useAuth } from "@/hooks/useAuth";

export default function Auth() {
  const location = useLocation();
  const isRegister = location.pathname === "/register";
  const navigate = useNavigate();
  const { login, register: registerUser, isLoginPending, isRegisterPending } = useAuth();

  const loginForm = useForm<LoginInput>({ resolver: zodResolver(loginSchema) });
  const registerForm = useForm<RegisterInput>({ resolver: zodResolver(registerSchema) });

  const handleLogin = async (data: LoginInput) => {
    await login(data);
    navigate("/");
  };

  const handleRegister = async (data: RegisterInput) => {
    await registerUser(data);
    navigate("/onboarding");
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <Link to="/" className="flex items-center justify-center gap-2 mb-2">
            <Globe className="h-6 w-6 text-primary" />
          </Link>
          <CardTitle>{isRegister ? "Create your account" : "Welcome back"}</CardTitle>
          <CardDescription>
            {isRegister
              ? "Start planning amazing trips today"
              : "Sign in to your Traveloop account"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isRegister ? (
            <form onSubmit={registerForm.handleSubmit(handleRegister)} className="flex flex-col gap-4">
              <Input
                label="Full name"
                error={registerForm.formState.errors.full_name?.message}
                {...registerForm.register("full_name")}
                placeholder="Jane Doe"
              />
              <Input
                label="Email"
                type="email"
                error={registerForm.formState.errors.email?.message}
                {...registerForm.register("email")}
                placeholder="you@example.com"
              />
              <Input
                label="Password"
                type="password"
                error={registerForm.formState.errors.password?.message}
                {...registerForm.register("password")}
                placeholder="Min. 8 characters"
              />
              <Input
                label="Confirm password"
                type="password"
                error={registerForm.formState.errors.confirm_password?.message}
                {...registerForm.register("confirm_password")}
                placeholder="Repeat password"
              />
              <Button type="submit" disabled={isRegisterPending} className="w-full">
                {isRegisterPending ? "Creating account…" : "Create account"}
              </Button>
              <Divider label="already have an account?" />
              <Link to="/login">
                <Button variant="outline" className="w-full">Sign in</Button>
              </Link>
            </form>
          ) : (
            <form onSubmit={loginForm.handleSubmit(handleLogin)} className="flex flex-col gap-4">
              <Input
                label="Email"
                type="email"
                error={loginForm.formState.errors.email?.message}
                {...loginForm.register("email")}
                placeholder="you@example.com"
              />
              <Input
                label="Password"
                type="password"
                error={loginForm.formState.errors.password?.message}
                {...loginForm.register("password")}
                placeholder="Your password"
              />
              <Button type="submit" disabled={isLoginPending} className="w-full">
                {isLoginPending ? "Signing in…" : "Sign in"}
              </Button>
              <Divider label="don't have an account?" />
              <Link to="/register">
                <Button variant="outline" className="w-full">Create account</Button>
              </Link>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
