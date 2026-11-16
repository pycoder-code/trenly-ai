# Внешние интеграции

- **Система:** Telegram. **Назначение:** Канал клиента: бот Trenly. **Протокол:** Bot API. **Часть:** `tg_bot`.
  **Решение:** [ADR 0006](adr/0006-telegram-bot-aiogram.md). **Документация:**
  [Bot API](https://core.telegram.org/bots/api)
- **Система:** OpenRouter, модель `google/gemini-3.8-flash`. **Назначение:** Распознавание КБЖУ по фото еды.
  **Протокол:** HTTPS, OpenAI-совместимый API. **Часть:** backend. **Решение:**
  [ADR 0004](adr/0004-macros-recognition-openrouter.md). **Документация:** [OpenRouter](https://openrouter.ai/docs)
- **Система:** Yandex Object Storage. **Назначение:** Хранение фото еды. Бот загружает JPEG, бэкенд читает объект и
  подписывает ссылки. **Протокол:** S3 API. **Часть:** `tg_bot`, backend. **Решение:**
  [ADR 0002](adr/0002-photo-storage.md). **Документация:** [Документация](https://yandex.cloud/ru/docs/storage/)
- **Система:** Платёжный провайдер (BR-007, нет в роадмапе). **Назначение:** Подписка тренера. **Часть:** backend.
  **Решение:** Предстоит
