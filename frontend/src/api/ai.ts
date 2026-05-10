import client from "./client";
import type {
  AIItineraryResponse,
  AIActivityResponse,
  AITransportResponse,
  AIFeedbackResponse,
  AIPackingResponse,
  AIChatResponse,
  AIGenerateInput,
  AISuggestActivitiesInput,
  AITransportInput,
  AIPackingInput,
  AIChatInput,
} from "@/types/ai";

const base = (tripSlug: string) => `/api/v1/ai/trips/${tripSlug}`;

export const aiApi = {
  generateItinerary: (tripSlug: string, data: AIGenerateInput) =>
    client.post<AIItineraryResponse>(`${base(tripSlug)}/generate-itinerary`, data),

  suggestActivities: (tripSlug: string, data: AISuggestActivitiesInput) =>
    client.post<AIActivityResponse>(`${base(tripSlug)}/suggest-activities`, data),

  recommendTransport: (tripSlug: string, data: AITransportInput) =>
    client.post<AITransportResponse>(`${base(tripSlug)}/recommend-transport`, data),

  reviewTrip: (tripSlug: string) =>
    client.post<AIFeedbackResponse>(`${base(tripSlug)}/review`),

  packingAdvice: (tripSlug: string, data: AIPackingInput) =>
    client.post<AIPackingResponse>(`${base(tripSlug)}/packing-advice`, data),

  chat: (data: AIChatInput) => client.post<AIChatResponse>("/api/v1/ai/chat", data),
};
