import Aura from "@primeuix/themes/aura";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { createApp } from "vue";

import App from "./App.vue";
import { router } from "./router";
import { useAuthStore } from "./stores/useAuthStore";
import "./style.css";

document.documentElement.classList.add("app-dark");

async function start() {
  const app = createApp(App);
  app.config.errorHandler = (error) => {
    console.error(error);
  };
  app.use(createPinia());
  await useAuthStore().restore();
  app.use(router);
  app.use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        darkModeSelector: "html.app-dark",
      },
    },
  });
  app.mount("#app");
}

void start();
