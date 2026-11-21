import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import PrimeVue from "primevue/config";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createMemoryHistory } from "vue-router";

import { createDashboardRouter } from "../router";
import { useAuthStore } from "../stores/useAuthStore";
import ClientListView from "./ClientListView.vue";

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

async function renderList() {
  const pinia = createPinia();
  setActivePinia(pinia);
  const auth = useAuthStore();
  auth.accessToken = "access";
  const router = createDashboardRouter(createMemoryHistory());
  const wrapper = mount(ClientListView, {
    attachTo: document.body,
    global: {
      plugins: [pinia, router, PrimeVue],
    },
  });
  await flushPromises();
  return { wrapper, router };
}

beforeEach(() => {
  document.body.innerHTML = "";
  localStorage.clear();
  get.mockReset();
});

describe("ClientListView", () => {
  it("показывает имя тренера и только пришедших клиентов", async () => {
    get.mockResolvedValueOnce({ data: trainer, response: jsonResponse(200, trainer) }).mockResolvedValueOnce({
      data: [{ id: 1, first_name: "Елена", last_name: "Волкова", phone: null, weight: null, active: true }],
      response: jsonResponse(200, []),
    });

    const { wrapper } = await renderList();

    expect(wrapper.text()).toContain("Иван Петров");
    expect(wrapper.text()).toContain("Тренер");
    expect(wrapper.text()).toContain("ИП");
    expect(wrapper.text()).toContain("Волкова Елена");
    expect(wrapper.text()).not.toContain("Сидоров Чужой");
    expect(wrapper.text()).toContain("Пригласить нового клиента");
    expect(wrapper.text()).toContain("На дашборд");
    wrapper.unmount();
  });

  it("пустой список не зовёт приглашать клиента", async () => {
    get
      .mockResolvedValueOnce({ data: trainer, response: jsonResponse(200, trainer) })
      .mockResolvedValueOnce({ data: [], response: jsonResponse(200, []) });

    const { wrapper } = await renderList();

    expect(wrapper.text()).toContain("Клиентов пока нет");
    expect(wrapper.text()).not.toContain("Пригласите");
    wrapper.unmount();
  });

  it("с фото показывает снимок вместо инициалов", async () => {
    const withPhoto = { ...trainer, photo: "https://photos.example/face.jpg" };
    get
      .mockResolvedValueOnce({ data: withPhoto, response: jsonResponse(200, withPhoto) })
      .mockResolvedValueOnce({ data: [], response: jsonResponse(200, []) });

    const { wrapper } = await renderList();

    expect(wrapper.find("img.avatar").attributes("src")).toBe("https://photos.example/face.jpg");
    expect(wrapper.text()).not.toContain("ИП");
    wrapper.unmount();
  });

  it("ссылка на дашборд открывает сегодняшний экран", async () => {
    get.mockResolvedValueOnce({ data: trainer, response: jsonResponse(200, trainer) }).mockResolvedValueOnce({
      data: [],
      response: jsonResponse(200, []),
    });
    const { wrapper, router } = await renderList();

    await wrapper.get("a.back").trigger("click");
    await flushPromises();

    expect(router.currentRoute.value.name).toBe("DashboardView");
    wrapper.unmount();
  });
});
