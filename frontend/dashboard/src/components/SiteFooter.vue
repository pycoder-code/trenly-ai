<template>
  <footer class="footer">
    <span>Trenly</span>
    <span class="muted">© Trenly · Все права защищены</span>
  </footer>
</template>

<style scoped>
.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-sizing: border-box;
  width: 100%;
  padding-inline: 24px;
  min-height: 88px;
  border-top: 1px solid #2a2a2a;
  color: #d4d4d4;
}

.muted {
  color: #8d8d8d;
  font-size: 14px;
}

@media (max-width: 720px) {
  .footer {
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
  }
}
</style>
