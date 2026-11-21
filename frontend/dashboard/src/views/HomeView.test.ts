import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import PrimeVue from "primevue/config";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createMemoryHistory } from "vue-router";

import { createDashboardRouter } from "../router";
import { useAuthStore } from "../stores/useAuthStore";
import HomeView from "./HomeView.vue";

const post = vi.hoisted(() => vi.fn());

vi.mock("api-client", () => ({
  createApiClient: () => ({
    POST: post,
    GET: vi.fn(),
  }),
}));

function jsonResponse(status: number, body: unknown) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

async function renderHome() {
  const pinia = createPinia();
  setActivePinia(pinia);
  const router = createDashboardRouter(createMemoryHistory());
  await router.push("/");
  await router.isReady();
  const wrapper = mount(HomeView, {
    attachTo: document.body,
    global: {
      plugins: [pinia, router, PrimeVue],
    },
  });
  return { wrapper, router };
}

beforeEach(() => {
  document.body.innerHTML = "";
  localStorage.clear();
  post.mockReset();
});

describe("HomeView", () => {
  it("логотип без входа ведёт на главную, со входом — на дашборд", async () => {
    const { wrapper } = await renderHome();
    expect(wrapper.get("a.brand").attributes("href")).toBe("/");

    const auth = useAuthStore();
    auth.accessToken = "access";
    await flushPromises();
    expect(wrapper.get("a.brand").attributes("href")).toBe("/dashboard");
    wrapper.unmount();
  });

  it("закрытие формы оставляет главную", async () => {
    const { wrapper, router } = await renderHome();

    await wrapper.get("button").trigger("click");
    expect(document.body.textContent).toContain("Вход в Trenly");

    document.body.querySelector<HTMLButtonElement>("[aria-label=Закрыть]")?.click();
    await flushPromises();

    expect(document.body.textContent).not.toContain("Вход в Trenly");
    expect(router.currentRoute.value.name).toBe("HomeView");
    wrapper.unmount();
  });

  it("успешный вход открывает дашборд", async () => {
    post.mockResolvedValue({
      data: { access_token: "access", refresh_token: "refresh" },
      response: jsonResponse(201, {}),
    });
    const { wrapper, router } = await renderHome();
    await wrapper.get("button").trigger("click");
    const phone = document.querySelector<HTMLInputElement>("#login-phone");
    const password = document.querySelector<HTMLInputElement>("#login-password");
    if (!phone || !password) {
      throw new Error("Поля входа не найдены");
    }
    phone.value = "+79990001122";
    phone.dispatchEvent(new Event("input"));
    password.value = "secret";
    password.dispatchEvent(new Event("input"));

    document.querySelector<HTMLButtonElement>("button[type=submit]")?.click();
    await flushPromises();

    expect(router.currentRoute.value.name).toBe("DashboardView");
    wrapper.unmount();
  });

  it("отказ входа оставляет форму и показывает причину", async () => {
    post.mockResolvedValue({
      data: undefined,
      response: jsonResponse(401, { detail: "Неверные учётные данные." }),
    });
    const { wrapper, router } = await renderHome();
    await wrapper.get("button").trigger("click");

    document.querySelector<HTMLButtonElement>("button[type=submit]")?.click();
    await flushPromises();

    expect(document.body.textContent).toContain("Неверные учётные данные.");
    expect(document.body.textContent).toContain("Вход в Trenly");
    expect(router.currentRoute.value.name).toBe("HomeView");
    wrapper.unmount();
  });

  it("заблокированный тренер остаётся на форме", async () => {
    // Кабинет не отличает блок от неверного пароля: API отвечает тем же 401.
    post.mockResolvedValue({
      data: undefined,
      response: jsonResponse(401, { detail: "Неверные учётные данные." }),
    });
    const { wrapper, router } = await renderHome();
    await wrapper.get("button").trigger("click");
    const phone = document.querySelector<HTMLInputElement>("#login-phone");
    const password = document.querySelector<HTMLInputElement>("#login-password");
    if (!phone || !password) {
      throw new Error("Поля входа не найдены");
    }
    phone.value = "+79990001122";
    phone.dispatchEvent(new Event("input"));
    password.value = "secret";
    password.dispatchEvent(new Event("input"));

    document.querySelector<HTMLButtonElement>("button[type=submit]")?.click();
    await flushPromises();

    expect(document.body.textContent).toContain("Вход в Trenly");
    expect(router.currentRoute.value.name).toBe("HomeView");
    wrapper.unmount();
  });
});
