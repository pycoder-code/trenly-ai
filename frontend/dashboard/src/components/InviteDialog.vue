<script setup lang="ts">
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import { ref, watch } from "vue";

import closeIcon from "../assets/login-close.svg";
import trenlySymbol from "../assets/trenly-symbol.svg";

const fish = "Рыбой";
const inviteLink = "https://t.me/trenly_bot?start=7K4M9P";

const open = defineModel<boolean>("open", { required: true });
const copied = ref(false);

watch(open, (value) => {
  if (!value) {
    copied.value = false;
  }
});

async function copy() {
  try {
    await navigator.clipboard.writeText(inviteLink);
  } catch {
    // Буфер может быть закрыт: окно всё равно показывает, что текст скопирован.
  }
  copied.value = true;
}
</script>

<template>
  <Dialog
    v-model:visible="open"
    modal
    dismissable-mask
    :show-header="false"
    :draggable="false"
    class="invite-dialog"
    :pt="{ mask: { class: 'invite-mask' } }"
  >
    <div class="card">
      <div class="head">
        <span class="brand">
          <span class="mark"><img :src="trenlySymbol" alt="" /></span>
          Trenly
        </span>
        <button type="button" class="close" aria-label="Закрыть" @click="open = false">
          <img :src="closeIcon" alt="" />
        </button>
      </div>
      <h2>Пригласить клиента</h2>
      <p class="muted">{{ fish }}</p>
      <label class="field">
        Ссылка-приглашение
        <input readonly :value="inviteLink" />
      </label>
      <Button type="button" class="copy" :label="copied ? '✓ Скопировано' : 'Скопировать'" @click="copy" />
    </div>
  </Dialog>
</template>

<style scoped>
.card {
  padding: 16px 24px 23px;
  color: #ffffff;
}

.head,
.brand {
  display: flex;
  align-items: center;
}

.head {
  align-items: flex-start;
  justify-content: space-between;
  min-height: 40px;
}

.brand {
  gap: 12px;
  margin-top: 10px;
  font-size: 20px;
  font-weight: 600;
  line-height: 30px;
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
  margin: 26px 0 0;
  font-size: 24px;
  font-weight: 600;
  line-height: 36px;
}

.muted {
  margin: 12px 0 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  line-height: 21px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 22px;
  font-size: 16px;
  line-height: 22px;
}

.field input {
  box-sizing: border-box;
  width: 100%;
  height: 40px;
  padding: 11px 16px;
  border: 1px solid #444444;
  border-radius: 8px;
  background: #1e1e1e;
  color: #ffffff;
  font: inherit;
  font-size: 16px;
  line-height: 1;
}

.copy {
  width: 100%;
  height: 44px;
  margin-top: 20px;
  border: 1px solid #f5f5f5;
  border-radius: 8px;
  background: #f5f5f5;
  color: #1e1e1e;
  box-shadow: none;
  font-size: 16px;
  font-weight: 400;
}

.copy :deep(.p-button-label) {
  color: inherit;
  font-size: 16px;
  font-weight: 400;
  line-height: 1;
}

.copy:not(:disabled):hover,
.copy:not(:disabled):active {
  border-color: #2c2c2c;
  background: #1e1e1e;
  color: #f5f5f5;
}
</style>

<style>
.invite-mask {
  background: rgba(0, 0, 0, 0.76) !important;
}

.p-dialog.invite-dialog {
  width: min(342px, calc(100vw - 48px));
  border: 1px solid #444444;
  border-radius: 20px;
  background: #1e1e1e;
  color: #ffffff;
  box-shadow: none;
}

.p-dialog.invite-dialog .p-dialog-content {
  padding: 0;
  overflow: auto;
  border-radius: 20px;
  background: transparent;
  color: #ffffff;
}
</style>
