import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

const post = vi.hoisted(() => vi.fn());
const get = vi.hoisted(() => vi.fn());

vi.mock("api-client", () => ({
  createApiClient: () => ({
    POST: post,
    GET: get,
  }),
}));

import { useAuthStore } from "./useAuthStore";

const refreshStorageKey = "trenly-trainer-refresh-token";

function jsonResponse(status: number, body: unknown) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

beforeEach(() => {
  localStorage.clear();
  post.mockReset();
  get.mockReset();
  setActivePinia(createPinia());
});

describe("useAuthStore", () => {
  it("сохраняет пару после успешного входа", async () => {
    post.mockResolvedValue({
      data: { access_token: "access", refresh_token: "refresh" },
      response: jsonResponse(201, { access_token: "access", refresh_token: "refresh" }),
    });
    const auth = useAuthStore();

    const result = await auth.login("+79990001122", "secret");

    expect(result).toEqual({ ok: true });
    expect(auth.accessToken).toBe("access");
    expect(localStorage.getItem(refreshStorageKey)).toBe("refresh");
  });

  it("не пишет пару и не обновляет её при отказе входа", async () => {
    post.mockResolvedValue({
      data: undefined,
      response: jsonResponse(401, { detail: "Неверные учётные данные." }),
    });
    const auth = useAuthStore();

    const result = await auth.login("+79990001122", "wrong");

    expect(result).toEqual({ ok: false, detail: "Неверные учётные данные." });
    expect(auth.accessToken).toBeNull();
    expect(localStorage.getItem(refreshStorageKey)).toBeNull();
    expect(post).toHaveBeenCalledTimes(1);
  });

  it("стирает сессию, если обмен токена обновления не удался", async () => {
    localStorage.setItem(refreshStorageKey, "stale");
    post.mockResolvedValue({
      data: undefined,
      response: jsonResponse(401, { detail: "Неверные учётные данные." }),
    });
    const auth = useAuthStore();

    await expect(auth.restore()).resolves.toBe(false);

    expect(auth.accessToken).toBeNull();
    expect(localStorage.getItem(refreshStorageKey)).toBeNull();
  });

  it("параллельное восстановление сессии обменивает токен один раз", async () => {
    localStorage.setItem(refreshStorageKey, "refresh");
    let finish: (value: unknown) => void = () => {};
    post.mockReturnValue(
      new Promise((resolve) => {
        finish = resolve;
      }),
    );
    const auth = useAuthStore();

    const first = auth.restore();
    const second = auth.restore();
    finish({
      data: { access_token: "access", refresh_token: "next" },
      response: jsonResponse(201, {}),
    });

    await expect(first).resolves.toBe(true);
    await expect(second).resolves.toBe(true);
    expect(post).toHaveBeenCalledTimes(1);
    expect(auth.accessToken).toBe("access");
  });

  it("выход очищает оба токена", async () => {
    post.mockResolvedValue({
      data: { access_token: "access", refresh_token: "refresh" },
      response: jsonResponse(201, {}),
    });
    const auth = useAuthStore();
    await auth.login("+79990001122", "secret");

    auth.logout();

    expect(auth.accessToken).toBeNull();
    expect(localStorage.getItem(refreshStorageKey)).toBeNull();
  });

  it("один раз обновляет пару после отказа чтения кабинета", async () => {
    post.mockResolvedValue({
      data: { access_token: "next-access", refresh_token: "next-refresh" },
      response: jsonResponse(201, {}),
    });
    get
      .mockResolvedValueOnce({
        data: undefined,
        response: jsonResponse(401, { detail: "Неверные учётные данные." }),
      })
      .mockResolvedValueOnce({
        data: { first_name: "Иван", last_name: "Петров", photo: null },
        response: jsonResponse(200, {}),
      });
    localStorage.setItem(refreshStorageKey, "refresh");
    const auth = useAuthStore();
    auth.accessToken = "expired";

    const result = await auth.loadTrainer();

    expect(result.response.status).toBe(200);
    expect(result.data).toEqual({ first_name: "Иван", last_name: "Петров", photo: null });
    expect(get).toHaveBeenCalledTimes(2);
    expect(post).toHaveBeenCalledTimes(1);
    expect(auth.accessToken).toBe("next-access");
  });
});
