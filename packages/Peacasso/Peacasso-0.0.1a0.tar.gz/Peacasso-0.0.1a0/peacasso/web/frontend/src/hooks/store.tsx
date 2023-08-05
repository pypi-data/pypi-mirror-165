import create from "zustand";

interface AppState {
  serverUrl: string;
  setServerUrl: (url: string) => void;
}

export const useStore = create<AppState>((set: any) => ({
  serverUrl: "http://127.0.0.1:8080/api",
  setServerUrl: (url: any) => set(() => ({ serverUrl: url })),
}));
