import { createRouter, createWebHistory, type RouterHistory } from "vue-router";

import { useAuthStore } from "./stores/useAuthStore";
import ClientListView from "./views/ClientListView.vue";
import DashboardView from "./views/DashboardView.vue";
import HomeView from "./views/HomeView.vue";

export function createDashboardRouter(history: RouterHistory = createWebHistory()) {
  const router = createRouter({
    history,
    routes: [
      { path: "/", name: "HomeView", component: HomeView },
      { path: "/dashboard", name: "DashboardView", component: DashboardView },
      { path: "/clients", name: "ClientListView", component: ClientListView },
    ],
  });

  router.beforeEach(async (to) => {
    if (to.name !== "ClientListView" && to.name !== "DashboardView") {
      return true;
    }
    const auth = useAuthStore();
    if (auth.accessToken) {
      return true;
    }
    const restored = await auth.restore();
    if (!restored) {
      return { name: "HomeView" };
    }
    return true;
  });

  return router;
}

export const router = createDashboardRouter();
