<script setup lang="ts">
import Button from "primevue/button";
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";

import { trainerMark } from "../cabinet";
import InviteDialog from "./InviteDialog.vue";
import TrenlyMark from "./TrenlyMark.vue";

const props = defineProps<{
  firstName: string;
  lastName: string;
  photo: string | null;
}>();

const emit = defineEmits<{
  logout: [];
}>();

const menuOpen = ref(false);
const inviteOpen = ref(false);
const mark = computed(() =>
  trainerMark({ first_name: props.firstName, last_name: props.lastName, photo: props.photo }),
);

function closeMenu() {
  menuOpen.value = false;
}

function openInvite() {
  menuOpen.value = false;
  inviteOpen.value = true;
}
</script>

<template>
  <header class="shell" :class="{ open: menuOpen }">
    <div class="bar">
      <div class="start">
        <RouterLink class="brand" :to="{ name: 'DashboardView' }"><TrenlyMark /> Trenly</RouterLink>
        <nav class="nav" aria-label="Кабинет">
          <RouterLink :to="{ name: 'ClientListView' }">Список клиентов</RouterLink>
          <button type="button" class="invite" @click="openInvite">Пригласить нового клиента</button>
        </nav>
      </div>
      <div class="account">
        <img v-if="mark.kind === 'photo'" class="avatar" :src="mark.url" alt="" />
        <span v-else class="avatar" aria-hidden="true">{{ mark.text }}</span>
        <span class="who">
          <span class="name">{{ firstName }} {{ lastName }}</span>
          <span class="role">Тренер</span>
        </span>
        <Button label="Выйти" class="logout" text @click="emit('logout')" />
      </div>
      <div class="tools">
        <Button label="Выйти" class="logout" text @click="emit('logout')" />
        <button
          type="button"
          class="burger"
          :aria-expanded="menuOpen"
          :aria-label="menuOpen ? 'Закрыть меню' : 'Открыть меню'"
          @click="menuOpen = !menuOpen"
        >
          <svg v-if="menuOpen" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M5 5l10 10M15 5L5 15" fill="none" stroke="currentColor" stroke-width="1.5" />
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M3 5h14M3 10h14M3 15h14" fill="none" stroke="currentColor" stroke-width="1.5" />
          </svg>
        </button>
      </div>
    </div>
    <div class="mobile-who">
      <img v-if="mark.kind === 'photo'" class="avatar" :src="mark.url" alt="" />
      <span v-else class="avatar" aria-hidden="true">{{ mark.text }}</span>
      <span class="who">
        <span class="name">{{ firstName }} {{ lastName }}</span>
        <span class="role">Тренер</span>
      </span>
    </div>
    <nav v-if="menuOpen" class="sheet" aria-label="Меню кабинета">
      <RouterLink :to="{ name: 'ClientListView' }" @click="closeMenu">Список клиентов</RouterLink>
      <button type="button" class="invite" @click="openInvite">Пригласить нового клиента</button>
    </nav>
    <button v-if="menuOpen" type="button" class="mask" aria-label="Закрыть меню" @click="closeMenu" />
    <InviteDialog v-model:open="inviteOpen" />
  </header>
</template>

<style scoped>
.shell {
  position: relative;
  z-index: 2;
}

.bar,
.start,
.brand,
.account,
.tools,
.mobile-who,
.who {
  display: flex;
  align-items: center;
}

.bar {
  justify-content: space-between;
  gap: 24px;
  box-sizing: border-box;
  width: 100%;
  min-height: 96px;
  padding-inline: 24px;
  border-bottom: 1px solid #2a2a2a;
}

.start {
  gap: 40px;
  min-width: 0;
}

.brand {
  gap: 12px;
  color: inherit;
  font-size: 28px;
  font-weight: 600;
  text-decoration: none;
}

.nav,
.sheet {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav a,
.nav button,
.sheet a,
.sheet button {
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  margin: 0;
  padding: 0;
  border: 1px solid transparent;
  border-radius: 8px;
  background: transparent;
  color: #e3e3e3;
  font: inherit;
  font-size: 16px;
  font-weight: 400;
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
}

.nav a,
.nav button {
  padding-inline: 24px;
}

.nav a:hover,
.nav button:hover,
.nav a:active,
.nav button:active,
.sheet a:hover,
.sheet button:hover,
.sheet a:active,
.sheet button:active {
  border-color: transparent;
  background: #444444;
  color: #ffffff;
}

.account,
.tools {
  gap: 12px;
}

.tools,
.mobile-who,
.sheet,
.mask {
  display: none;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  background: #3a3a3a;
  display: grid;
  place-items: center;
  font-size: 14px;
  flex: 0 0 44px;
}

.who {
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.role {
  color: #a3a3a3;
  font-size: 14px;
}

.logout {
  border: 1px solid transparent;
  background: transparent;
  color: #ffffff;
  box-shadow: none;
}

.logout :deep(.p-button-label) {
  color: inherit;
  font-weight: 400;
}

.logout:not(:disabled):hover,
.logout:not(:disabled):active {
  border-color: transparent;
  background: transparent;
  color: #ffffff;
}

.burger {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border: 0;
  border-radius: 8px;
  background: #2c2c2c;
  color: #ffffff;
  cursor: pointer;
}

.sheet {
  flex-direction: column;
  padding: 20px 24px;
  background: #1e1e1e;
  border-radius: 0 0 20px 20px;
}

.sheet a,
.sheet button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  border-color: #444444;
}

.sheet a:hover,
.sheet button:hover,
.sheet a:active,
.sheet button:active {
  border-color: #444444;
}

.mask {
  position: fixed;
  inset: 0;
  z-index: 1;
  border: 0;
  background: rgba(0, 0, 0, 0.72);
  cursor: pointer;
}

@media (max-width: 720px) {
  .nav,
  .account {
    display: none;
  }

  .tools {
    display: flex;
  }

  .bar {
    min-height: 80px;
  }

  .mobile-who {
    display: flex;
    gap: 12px;
    padding: 16px 24px 0;
  }

  .shell.open .mobile-who {
    display: none;
  }

  .shell.open .bar,
  .shell.open .sheet {
    position: relative;
    z-index: 2;
    background: #1e1e1e;
  }

  .shell.open .bar {
    border-bottom-color: transparent;
  }

  .shell.open .sheet,
  .shell.open .mask {
    display: flex;
  }
}
</style>
