import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import PrimeVue from "primevue/config";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createMemoryHistory } from "vue-router";

import { createDashboardRouter } from "../router";
import { useAuthStore } from "../stores/useAuthStore";
import DashboardView from "./DashboardView.vue";

const get = vi.hoisted(() => vi.fn());

vi.mock("api-client", () => ({
  createApiClient: () => ({
    POST: vi.fn(),
    GET: get,
  }),
}));

function jsonResponse(status: number, body: unknown) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

const trainer = { first_name: "Иван", last_name: "Петров", photo: null };

beforeEach(() => {
  document.body.innerHTML = "";
  localStorage.clear();
  get.mockReset();
});

describe("DashboardView", () => {
  it("без входа остаётся на главной", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const router = createDashboardRouter(createMemoryHistory());
    await router.push("/dashboard");
    await router.isReady();

    expect(router.currentRoute.value.name).toBe("HomeView");
  });

  it("показывает пустой день и открывает список из меню", async () => {
    get.mockResolvedValue({ data: trainer, response: jsonResponse(200, trainer) });
    const pinia = createPinia();
    setActivePinia(pinia);
    const auth = useAuthStore();
    auth.accessToken = "access";
    const router = createDashboardRouter(createMemoryHistory());
    await router.push("/dashboard");
    await router.isReady();
    const wrapper = mount(DashboardView, {
      attachTo: document.body,
      global: { plugins: [pinia, router, PrimeVue] },
    });
    await flushPromises();

    expect(wrapper.get("a.brand").attributes("href")).toBe("/dashboard");
    expect(wrapper.text()).toContain("Занятий нет");
    expect(wrapper.text()).toContain("Сегодня у вас нет запланированных занятий.");
    expect(wrapper.find(".sheet").exists()).toBe(false);

    await wrapper.get("[aria-label='Открыть меню']").trigger("click");
    expect(wrapper.find(".sheet").exists()).toBe(true);
    expect(wrapper.get(".sheet").text()).toContain("Пригласить нового клиента");

    await wrapper.get(".sheet .invite").trigger("click");
    expect(router.currentRoute.value.name).toBe("DashboardView");
    expect(document.body.textContent).toContain("Пригласить клиента");
    expect(document.body.textContent).toContain("Рыбой");
    expect(document.querySelector<HTMLInputElement>(".invite-dialog input")?.value).toBe(
      "https://t.me/trenly_bot?start=7K4M9P",
    );

    document.body.querySelector<HTMLButtonElement>(".copy")?.click();
    await flushPromises();
    expect(document.body.textContent).toContain("Скопировано");
    expect(document.body.textContent).toContain("Рыбой");

    await wrapper.get(".nav a").trigger("click");
    await flushPromises();
    expect(router.currentRoute.value.name).toBe("ClientListView");
    wrapper.unmount();
  });

  it("выход возвращает на главную и закрывает список", async () => {
    get.mockResolvedValue({ data: trainer, response: jsonResponse(200, trainer) });
    const pinia = createPinia();
    setActivePinia(pinia);
    const auth = useAuthStore();
    auth.accessToken = "access";
    const router = createDashboardRouter(createMemoryHistory());
    await router.push("/dashboard");
    await router.isReady();
    const wrapper = mount(DashboardView, {
      attachTo: document.body,
      global: { plugins: [pinia, router, PrimeVue] },
    });
    await flushPromises();

    await wrapper.get(".account .logout").trigger("click");
    await flushPromises();

    expect(router.currentRoute.value.name).toBe("HomeView");
    await router.push("/clients");
    await flushPromises();
    expect(router.currentRoute.value.name).toBe("HomeView");
    wrapper.unmount();
  });
});
