<script setup lang="ts">
import Button from "primevue/button";
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";

import LoginDialog from "../components/LoginDialog.vue";
import SiteFooter from "../components/SiteFooter.vue";
import TrenlyMark from "../components/TrenlyMark.vue";
import { useAuthStore } from "../stores/useAuthStore";

const loginOpen = ref(false);
const auth = useAuthStore();
const logoTo = computed(() => (auth.accessToken ? { name: "DashboardView" } : { name: "HomeView" }));
</script>

<template>
  <div class="page">
    <header class="topbar">
      <RouterLink class="brand" :to="logoTo"><TrenlyMark /> Trenly</RouterLink>
      <Button label="Войти" class="enter" @click="loginOpen = true" />
    </header>
    <main class="hero">
      <h1>Всё для занятий.<br />В одном месте.</h1>
      <p>Расписание, клиенты и занятия — под рукой, без лишней рутины.</p>
      <Button label="Войти" class="enter" @click="loginOpen = true" />
    </main>
    <SiteFooter />
    <LoginDialog v-model:open="loginOpen" />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #141414;
}

.topbar,
.brand {
  display: flex;
  align-items: center;
}

.topbar {
  justify-content: space-between;
  box-sizing: border-box;
  width: 100%;
  padding-inline: 24px;
  min-height: 96px;
  border-bottom: 1px solid #2a2a2a;
}

.brand {
  gap: 12px;
  color: inherit;
  font-size: 28px;
  font-weight: 600;
  text-decoration: none;
}

.hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 24px 72px;
}

h1 {
  margin: 0;
  font-size: 64px;
  line-height: 1.05;
  font-weight: 650;
}

p {
  max-width: 360px;
  color: #bdbdbd;
  font-size: 18px;
  line-height: 1.4;
}

.enter {
  border: 1px solid #f5f5f5;
  border-radius: 12px;
  background: #f5f5f5;
  color: #1e1e1e;
}

.enter :deep(.p-button-label) {
  color: inherit;
}

.enter:not(:disabled):hover,
.enter:not(:disabled):active {
  background: #1e1e1e;
  border-color: #2c2c2c;
  color: #f5f5f5;
}

@media (max-width: 720px) {
  h1 {
    font-size: 40px;
  }
}
</style>
