import { create } from "zustand";

type ModalKey =
  | "addStop"
  | "editStop"
  | "addActivity"
  | "addNote"
  | "createTrip"
  | "confirmDelete"
  | null;

interface UIState {
  sidebarOpen: boolean;
  activeModal: ModalKey;
  modalData: Record<string, unknown>;
  theme: "light" | "dark";
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  openModal: (key: ModalKey, data?: Record<string, unknown>) => void;
  closeModal: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

export const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: false,
  activeModal: null,
  modalData: {},
  theme: "light",

  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  openModal: (key, data = {}) => set({ activeModal: key, modalData: data }),
  closeModal: () => set({ activeModal: null, modalData: {} }),

  setTheme: (theme) => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    set({ theme });
  },
}));
