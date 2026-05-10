import { create } from "zustand";
import type { AIChatMessage } from "@/types/ai";

interface AIState {
  chatHistory: AIChatMessage[];
  isChatOpen: boolean;
  isLoading: boolean;
  addMessage: (msg: AIChatMessage) => void;
  setLoading: (loading: boolean) => void;
  toggleChat: () => void;
  setChatOpen: (open: boolean) => void;
  clearHistory: () => void;
}

export const useAIStore = create<AIState>()((set) => ({
  chatHistory: [],
  isChatOpen: false,
  isLoading: false,

  addMessage: (msg) =>
    set((state) => ({ chatHistory: [...state.chatHistory, msg] })),

  setLoading: (loading) => set({ isLoading: loading }),

  toggleChat: () => set((s) => ({ isChatOpen: !s.isChatOpen })),

  setChatOpen: (open) => set({ isChatOpen: open }),

  clearHistory: () => set({ chatHistory: [] }),
}));
