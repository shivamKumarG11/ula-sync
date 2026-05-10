import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import { Globe } from "lucide-react";
import client from "@/api/client";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { useAuthStore } from "@/store/authStore";
import type { UserUpdateInput } from "@/types/user";

const STEPS = ["Welcome", "About You", "Travel Style", "Home City", "Done"];

const TRAVEL_STYLES = ["Budget", "Backpacker", "Mid-range", "Luxury", "Adventure", "Cultural", "Slow travel"];

export default function Onboarding() {
  const [step, setStep] = useState(0);
  const navigate = useNavigate();
  const { user } = useAuth();
  const setUser = useAuthStore((s) => s.setUser);
  const { register, handleSubmit, setValue, watch } = useForm<UserUpdateInput>({
    defaultValues: { preferred_currency: "USD" },
  });
  const selectedStyle = watch("travel_style");

  const onFinish = async (data: UserUpdateInput) => {
    const res = await client.put("/api/v1/users/me", data);
    setUser(res.data);
    navigate(`/u/${user?.username}/dashboard`);
  };

  const progress = ((step + 1) / STEPS.length) * 100;

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary/5 to-background p-4">
      <div className="w-full max-w-md">
        <div className="flex items-center gap-2 justify-center mb-8">
          <Globe className="h-6 w-6 text-primary" />
          <span className="font-bold text-lg">Traveloop</span>
        </div>
        <div className="h-1.5 w-full rounded-full bg-muted mb-8">
          <motion.div
            className="h-full rounded-full bg-primary"
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -30 }}
            transition={{ duration: 0.2 }}
            className="bg-background rounded-xl border p-8 shadow-sm"
          >
            {step === 0 && (
              <div className="text-center flex flex-col gap-4">
                <h2 className="text-2xl font-bold">Welcome to Traveloop! 🌍</h2>
                <p className="text-muted-foreground">
                  Let's set up your profile in a few quick steps so we can personalise your experience.
                </p>
                <Button onClick={() => setStep(1)}>Let's get started</Button>
              </div>
            )}

            {step === 1 && (
              <form className="flex flex-col gap-4">
                <h2 className="text-xl font-bold">About you</h2>
                <Input label="Full name" {...register("full_name")} placeholder="Jane Doe" />
                <Input label="Bio" {...register("bio")} placeholder="A short bio about yourself" />
                <Input label="Preferred currency" {...register("preferred_currency")} placeholder="USD" />
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={() => setStep(0)}>Back</Button>
                  <Button onClick={() => setStep(2)}>Continue</Button>
                </div>
              </form>
            )}

            {step === 2 && (
              <div className="flex flex-col gap-4">
                <h2 className="text-xl font-bold">Your travel style</h2>
                <div className="grid grid-cols-2 gap-2">
                  {TRAVEL_STYLES.map((style) => (
                    <button
                      key={style}
                      type="button"
                      onClick={() => setValue("travel_style", style)}
                      className={`rounded-lg border px-3 py-2 text-sm text-left transition-colors ${selectedStyle === style ? "border-primary bg-primary/10" : "hover:bg-muted"}`}
                    >
                      {style}
                    </button>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={() => setStep(1)}>Back</Button>
                  <Button onClick={() => setStep(3)}>Continue</Button>
                </div>
              </div>
            )}

            {step === 3 && (
              <form className="flex flex-col gap-4">
                <h2 className="text-xl font-bold">Where are you based?</h2>
                <Input label="Home city" {...register("home_city")} placeholder="e.g. Mumbai" />
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={() => setStep(2)}>Back</Button>
                  <Button onClick={() => setStep(4)}>Continue</Button>
                </div>
              </form>
            )}

            {step === 4 && (
              <div className="text-center flex flex-col gap-4">
                <h2 className="text-2xl font-bold">You're all set! 🎉</h2>
                <p className="text-muted-foreground">
                  Your profile is ready. Start exploring cities, create a trip, or browse the community.
                </p>
                <Button onClick={handleSubmit(onFinish)}>Go to my dashboard</Button>
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        <p className="text-center text-xs text-muted-foreground mt-4">
          Step {step + 1} of {STEPS.length}
        </p>
      </div>
    </div>
  );
}
