export interface AIItineraryDay {
  day: number;
  date: string;
  city: string;
  morning: string;
  afternoon: string;
  evening: string;
  tips: string;
}

export interface AIItineraryResponse {
  itinerary: AIItineraryDay[];
  summary: string;
  is_fallback?: boolean;
}

export interface AIActivitySuggestion {
  name: string;
  description: string;
  why: string;
  estimated_hours: number;
  estimated_cost_usd: number;
  category: string;
}

export interface AIActivityResponse {
  suggestions: AIActivitySuggestion[];
  is_fallback?: boolean;
}

export interface AITransportOption {
  mode: string;
  description: string;
  estimated_cost_usd: number;
  estimated_duration: string;
  pros: string[];
  cons: string[];
  recommended: boolean;
}

export interface AITransportResponse {
  options: AITransportOption[];
  recommendation: string;
  is_fallback?: boolean;
}

export interface AIFeedbackResponse {
  score: number;
  summary: string;
  strengths: string[];
  improvements: string[];
  seasonal_notes: string;
  is_fallback?: boolean;
}

export interface AIPackingItem {
  name: string;
  category: string;
  reason: string;
  essential: boolean;
}

export interface AIPackingResponse {
  items: AIPackingItem[];
  is_fallback?: boolean;
}

export interface AIChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface AIChatResponse {
  reply: string;
  actions: { label: string; url: string }[];
  is_fallback?: boolean;
}

export interface AIGenerateInput {
  preferences?: string;
}

export interface AISuggestActivitiesInput {
  city_slug: string;
  duration_days?: number;
  style?: string;
}

export interface AITransportInput {
  from_stop_id: number;
  to_stop_id: number;
}

export interface AIPackingInput {
  style?: string;
}

export interface AIChatInput {
  messages: AIChatMessage[];
  context?: string;
}
