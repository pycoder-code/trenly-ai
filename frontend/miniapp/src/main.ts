import { createApp } from "vue";

import App from "./App.vue";
import { router } from "./router";
import { applyTelegramTheme } from "./telegram";
import "./style.css";

applyTelegramTheme();

createApp(App).use(router).mount("#app");
