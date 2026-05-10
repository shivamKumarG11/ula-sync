import { create } from "zustand";
import { persist } from "zustand/middleware";

interface CurrencyState {
  preferred: string;
  rates: Record<string, number>;
  ratesUpdatedAt: number | null;
  setPreferred: (currency: string) => void;
  setRates: (rates: Record<string, number>) => void;
  convert: (amountUsd: number) => number;
}

export const useCurrencyStore = create<CurrencyState>()(
  persist(
    (set, get) => ({
      preferred: "USD",
      rates: {},
      ratesUpdatedAt: null,

      setPreferred: (currency) => set({ preferred: currency }),

      setRates: (rates) => set({ rates, ratesUpdatedAt: Date.now() }),

      convert: (amountUsd) => {
        const { preferred, rates } = get();
        if (preferred === "USD" || !rates[preferred]) return amountUsd;
        return amountUsd * rates[preferred];
      },
    }),
    {
      name: "traveloop-currency",
    },
  ),
);
