import { create } from "zustand";
import type { TripCreateInput } from "@/types/trip";

interface TripDraft extends Partial<TripCreateInput> {
  selectedCityIds: number[];
}

interface TripStoreState {
  draft: TripDraft;
  setDraft: (patch: Partial<TripDraft>) => void;
  resetDraft: () => void;
}

const EMPTY_DRAFT: TripDraft = {
  selectedCityIds: [],
};

export const useTripStore = create<TripStoreState>()((set) => ({
  draft: EMPTY_DRAFT,

  setDraft: (patch) =>
    set((state) => ({ draft: { ...state.draft, ...patch } })),

  resetDraft: () => set({ draft: EMPTY_DRAFT }),
}));
