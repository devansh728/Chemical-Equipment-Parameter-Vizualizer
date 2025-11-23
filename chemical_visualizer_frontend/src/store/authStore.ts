import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// interface AuthState {
//   token: string | null;
//   isAuthenticated: boolean;
//   login: (token: string) => void;
//   logout: () => void;
// }

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (token: string, refreshToken: string) => void;
  updateToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      login: (token: string, refreshToken: string) => set({ token, refreshToken, isAuthenticated: true }),
      updateToken: (token: string) => set({ token }),
      logout: () => set({ token: null, refreshToken: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
