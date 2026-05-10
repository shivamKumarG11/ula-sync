import { useMutation } from "@tanstack/react-query";
import { aiApi } from "@/api/ai";
import { useAIStore } from "@/store/aiStore";
import type {
  AIGenerateInput,
  AISuggestActivitiesInput,
  AITransportInput,
  AIPackingInput,
} from "@/types/ai";

export function useGenerateItinerary(tripSlug: string) {
  return useMutation({
    mutationFn: (data: AIGenerateInput) =>
      aiApi.generateItinerary(tripSlug, data).then((r) => r.data),
  });
}

export function useSuggestActivities(tripSlug: string) {
  return useMutation({
    mutationFn: (data: AISuggestActivitiesInput) =>
      aiApi.suggestActivities(tripSlug, data).then((r) => r.data),
  });
}

export function useRecommendTransport(tripSlug: string) {
  return useMutation({
    mutationFn: (data: AITransportInput) =>
      aiApi.recommendTransport(tripSlug, data).then((r) => r.data),
  });
}

export function useReviewTrip(tripSlug: string) {
  return useMutation({
    mutationFn: () => aiApi.reviewTrip(tripSlug).then((r) => r.data),
  });
}

export function usePackingAdvice(tripSlug: string) {
  return useMutation({
    mutationFn: (data: AIPackingInput) =>
      aiApi.packingAdvice(tripSlug, data).then((r) => r.data),
  });
}

export function useAIChat() {
  const { addMessage, setLoading } = useAIStore();

  return useMutation({
    mutationFn: (userMessage: string) => {
      const { chatHistory } = useAIStore.getState();
      addMessage({ role: "user", content: userMessage });
      return aiApi
        .chat({ messages: [...chatHistory, { role: "user", content: userMessage }] })
        .then((r) => r.data);
    },
    onMutate: () => setLoading(true),
    onSuccess: (data) => {
      addMessage({ role: "assistant", content: data.reply });
      setLoading(false);
    },
    onError: () => setLoading(false),
  });
}
