import type { IAuthState } from "@/shared/types/storeTypes";
import { create } from "zustand";

export const useAuthStore = create<IAuthState>(set => ({
    accessToken: null,
    setAccessToken: token => set({ accessToken: token }),
    logout: () => set({ accessToken: null }),
}));
