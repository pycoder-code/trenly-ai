<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import CabinetHeader from "../components/CabinetHeader.vue";
import SiteFooter from "../components/SiteFooter.vue";
import { useAuthStore } from "../stores/useAuthStore";

const auth = useAuthStore();
const router = useRouter();
const trainer = ref<{ first_name: string; last_name: string; photo: string | null } | null>(null);

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
    <main v-if="trainer" class="content">
      <h1>Сегодня</h1>
      <p class="lead">Клиенты, у которых сегодня тренировка.</p>
      <div class="empty">
        <p class="title">Занятий нет</p>
        <p class="note">Сегодня у вас нет запланированных занятий.</p>
      </div>
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

h1 {
  margin: 0;
  font-size: 40px;
  font-weight: 600;
  line-height: 58px;
}

.lead {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  line-height: 23px;
}

.empty {
  min-height: 408px;
  margin-top: 32px;
  border: 1px solid #444444;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 24px;
}

.title,
.note {
  margin: 0;
}

.title {
  font-size: 30px;
  font-weight: 600;
  line-height: 42px;
}

.note {
  margin-top: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  line-height: 22px;
}

@media (max-width: 720px) {
  h1 {
    font-size: 32px;
    line-height: 45px;
  }

  .empty {
    min-height: 356px;
  }
}
</style>
