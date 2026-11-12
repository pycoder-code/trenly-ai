import { init, themeParams } from "@tma.js/sdk-vue";

const fallbackBackground = "#e8e8e8";

export function applyTelegramTheme(): void {
  document.documentElement.style.setProperty("--tg-theme-bg-color", fallbackBackground);
  try {
    init();
    themeParams.mount();
    themeParams.bindCssVars();
  } catch {
    document.documentElement.style.setProperty("--tg-theme-bg-color", fallbackBackground);
  }
}
