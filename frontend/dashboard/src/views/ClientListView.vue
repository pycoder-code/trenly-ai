<script setup lang="ts">
import InputText from "primevue/inputtext";
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { clientCountLabel, clientName, visibleClients } from "../cabinet";
import type { NameParts } from "../cabinet";
import CabinetHeader from "../components/CabinetHeader.vue";
import SiteFooter from "../components/SiteFooter.vue";
import { useAuthStore } from "../stores/useAuthStore";

type ClientRow = NameParts & { id: number };

const auth = useAuthStore();
const router = useRouter();
const trainer = ref<{ first_name: string; last_name: string; photo: string | null } | null>(null);
const rows = ref<ClientRow[]>([]);
const query = ref("");
const ready = ref(false);

const shown = computed(() => visibleClients(rows.value, query.value));

async function leave() {
  auth.logout();
  await router.push({ name: "HomeView" });
}

onMounted(async () => {
  const trainerResult = await auth.loadTrainer();
  if (trainerResult.response.status !== 200 || !trainerResult.data) {
    await leave();
    return;
  }
  trainer.value = trainerResult.data;
  const clientsResult = await auth.loadClients();
  if (clientsResult.response.status !== 200 || !clientsResult.data) {
    await leave();
    return;
  }
  rows.value = clientsResult.data;
  ready.value = true;
});
</script>

<template>
  <div class="page">
    <CabinetHeader
      v-if="trainer"
      :first-name="trainer.first_name"
      :last-name="trainer.last_name"
      :photo="trainer.photo"
      @logout="leave"
    />
    <main v-if="ready" class="content">
      <RouterLink class="back" :to="{ name: 'DashboardView' }">← На дашборд</RouterLink>
      <h1>Список клиентов</h1>
      <p class="lead">Все ваши клиенты в одном списке.</p>
      <label v-if="rows.length" class="search">
        Поиск клиента
        <InputText v-model="query" placeholder="Фамилия или имя" fluid />
      </label>
      <div class="meta">
        <span>{{ clientCountLabel(shown.length) }}</span>
        <span v-if="rows.length" class="muted">По алфавиту, А–Я</span>
      </div>
      <ul v-if="rows.length" class="list">
        <li v-for="client in shown" :key="client.id">{{ clientName(client) }}</li>
      </ul>
      <div v-else class="empty">Клиентов пока нет</div>
    </main>
    <SiteFooter />
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #141414;
}

.content {
  box-sizing: border-box;
  width: 100%;
  flex: 1;
  padding: 28px 24px 48px;
}

.back {
  display: inline-flex;
  align-items: center;
  height: 40px;
  margin-bottom: 8px;
  color: #ffffff;
  font-size: 14px;
  line-height: 20px;
  text-decoration: none;
}

h1 {
  margin: 0 0 8px;
  font-size: 48px;
  font-weight: 650;
}

.lead,
.muted {
  color: #bdbdbd;
}

.lead {
  margin: 0 0 28px;
}

.search {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 480px;
}

.search :deep(.p-inputtext) {
  box-sizing: border-box;
  width: 100%;
  height: 40px;
  padding: 11px 16px;
  border: 1px solid #444444;
  border-radius: 8px;
  background: #1e1e1e;
  color: #ffffff;
  box-shadow: none;
  font-size: 16px;
  line-height: 1;
}

.search :deep(.p-inputtext::placeholder) {
  color: rgba(255, 255, 255, 0.7);
  opacity: 1;
}

.search :deep(.p-inputtext:enabled:hover),
.search :deep(.p-inputtext:enabled:focus) {
  background: #1e1e1e;
  border-color: #444444;
  outline: none;
  box-shadow: none;
}

.meta {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin: 28px 0 16px;
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list li,
.empty {
  border: 1px solid #3a3a3a;
  border-radius: 12px;
  background: #191919;
}

.list li {
  padding: 18px 20px;
}

.empty {
  min-height: 280px;
  display: grid;
  place-items: center;
  font-size: 28px;
  font-weight: 600;
}

@media (max-width: 720px) {
  h1 {
    font-size: 34px;
  }
}
</style>
