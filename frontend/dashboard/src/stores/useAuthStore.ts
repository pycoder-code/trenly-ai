import { createApiClient } from "api-client";
import { defineStore } from "pinia";
import { ref } from "vue";

const refreshStorageKey = "trenly-trainer-refresh-token";
const refusal = "Неверные учётные данные.";

type TokenPair = {
  access_token: string;
  refresh_token: string;
};

type CallResult<T> = {
  data?: T;
  response: Response;
};

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(localStorage.getItem(refreshStorageKey));
  const client = createApiClient("", () => accessToken.value);
  let pendingRestore: Promise<boolean> | null = null;

  function persist(pair: TokenPair) {
    accessToken.value = pair.access_token;
    refreshToken.value = pair.refresh_token;
    localStorage.setItem(refreshStorageKey, pair.refresh_token);
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem(refreshStorageKey);
  }

  async function refusalDetail(response: Response) {
    try {
      const body: unknown = await response.clone().json();
      if (body && typeof body === "object" && "detail" in body && typeof body.detail === "string" && body.detail) {
        return body.detail;
      }
    } catch {
      // Тело отказа не JSON: остаётся общая фраза.
    }
    return refusal;
  }

  async function login(phone: string, password: string) {
    const result = await client.POST("/api/access-tokens", { body: { phone, password } });
    if (result.response.status === 201 && result.data) {
      persist(result.data);
      return { ok: true as const };
    }
    return { ok: false as const, detail: await refusalDetail(result.response) };
  }

  async function refresh() {
    if (!refreshToken.value) {
      return false;
    }
    const result = await client.POST("/api/refresh-tokens", {
      body: { refresh_token: refreshToken.value },
    });
    if (result.response.status === 201 && result.data) {
      persist(result.data);
      return true;
    }
    logout();
    return false;
  }

  function restore() {
    if (accessToken.value) {
      return Promise.resolve(true);
    }
    if (!pendingRestore) {
      pendingRestore = refresh().finally(() => {
        pendingRestore = null;
      });
    }
    return pendingRestore;
  }

  async function authorized<T>(run: () => Promise<CallResult<T>>) {
    const first = await run();
    if (first.response.status !== 401) {
      return first;
    }
    const renewed = await refresh();
    if (!renewed) {
      return first;
    }
    return run();
  }

  function loadTrainer() {
    return authorized(() => client.GET("/api/trainers/me"));
  }

  function loadClients() {
    return authorized(() => client.GET("/api/clients"));
  }

  return { accessToken, login, logout, restore, loadTrainer, loadClients };
});
