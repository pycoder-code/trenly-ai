<script setup lang="ts">
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import { ref } from "vue";
import { useRouter } from "vue-router";

import closeIcon from "../assets/login-close.svg";
import trenlySymbol from "../assets/trenly-symbol.svg";
import { useAuthStore } from "../stores/useAuthStore";

const open = defineModel<boolean>("open", { required: true });

const phone = ref("");
const password = ref("");
const detail = ref("");
const pending = ref(false);
const auth = useAuthStore();
const router = useRouter();

async function submit() {
  if (pending.value) {
    return;
  }
  pending.value = true;
  detail.value = "";
  const result = await auth.login(phone.value, password.value);
  pending.value = false;
  if (!result.ok) {
    detail.value = result.detail;
    return;
  }
  open.value = false;
  await router.push({ name: "DashboardView" });
}
</script>

<template>
  <Dialog
    v-model:visible="open"
    modal
    dismissable-mask
    :show-header="false"
    :draggable="false"
    class="login-dialog"
    :pt="{ mask: { class: 'login-mask' } }"
  >
    <form class="form" @submit.prevent="submit">
      <div class="form-head">
        <span class="brand">
          <span class="mark"><img :src="trenlySymbol" alt="" /></span>
          Trenly
        </span>
        <button type="button" class="close" aria-label="Закрыть" @click="open = false">
          <img :src="closeIcon" alt="" />
        </button>
      </div>
      <h2>Вход в Trenly</h2>
      <p class="muted">Вернитесь к своим занятиям.</p>
      <div class="fields">
        <label class="field">
          Телефон
          <InputText id="login-phone" v-model="phone" placeholder="+7 999 123-45-67" autocomplete="username" fluid />
        </label>
        <label class="field">
          Пароль
          <Password
            v-model="password"
            input-id="login-password"
            placeholder="••••••••"
            aria-label="Пароль"
            :feedback="false"
            :toggle-mask="false"
            autocomplete="current-password"
            fluid
          />
        </label>
        <p v-if="detail" class="detail" role="alert">{{ detail }}</p>
        <Button type="submit" label="Войти" class="submit" :loading="pending" fluid />
      </div>
    </form>
  </Dialog>
</template>

<style scoped>
.form {
  padding: 15px 24px 33px;
  color: #ffffff;
}

.form-head,
.brand {
  display: flex;
  align-items: center;
}

.form-head {
  align-items: flex-start;
  justify-content: space-between;
  min-height: 40px;
}

.brand {
  gap: 12px;
  margin-top: 10px;
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
}

.mark {
  position: relative;
  width: 28px;
  height: 28px;
  flex: 0 0 28px;
}

.mark img {
  position: absolute;
  top: 18.75%;
  left: 15.63%;
}

.close {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

h2 {
  margin: 22px 0 0;
  font-size: 26px;
  font-weight: 600;
  line-height: 36px;
}

.muted {
  margin: 4px 0 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  line-height: 20px;
}

.fields {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 28px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 16px;
  line-height: 1.4;
}

.field :deep(.p-inputtext) {
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

.field :deep(.p-inputtext::placeholder) {
  color: #ffffff;
  opacity: 1;
}

.field :deep(.p-inputtext:enabled:focus) {
  border-color: #f5f5f5;
  outline: none;
  box-shadow: none;
}

.detail {
  margin: 0;
  color: #f0b4b4;
  font-size: 14px;
  line-height: 1.4;
}

.submit {
  height: 44px;
  border: 1px solid #f5f5f5;
  border-radius: 8px;
  background: #f5f5f5;
  color: #1e1e1e;
  box-shadow: none;
  font-size: 16px;
  font-weight: 400;
}

.submit :deep(.p-button-label) {
  color: inherit;
  font-size: 16px;
  font-weight: 400;
  line-height: 1;
}

.submit:not(:disabled):hover,
.submit:not(:disabled):active {
  border-color: #2c2c2c;
  background: #1e1e1e;
  color: #f5f5f5;
}
</style>

<style>
/* Фон маски задан в style темы, обычное правило его не перекрывает. */
.login-mask {
  background: rgba(0, 0, 0, 0.76) !important;
}

.p-dialog.login-dialog {
  width: min(440px, calc(100vw - 48px));
  border: 1px solid #444444;
  border-radius: 20px;
  background: #1e1e1e;
  color: #ffffff;
  box-shadow: none;
}

.p-dialog.login-dialog .p-dialog-content {
  padding: 0;
  overflow: auto;
  border-radius: 20px;
  background: transparent;
  color: #ffffff;
}
</style>
