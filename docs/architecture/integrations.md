# Внешние интеграции

| Система | Назначение | Протокол | Часть | Решение | Документация |
|---|---|---|---|---|---|
| Telegram | Канал клиента: бот Trenly | Bot API | backend | — | [Bot API](https://core.telegram.org/bots/api) |
| OpenRouter, модель `google/gemini-3.8-flash` | Распознавание КБЖУ по фото еды | HTTPS, OpenAI-совместимый API | backend | [ADR 0004](adr/0004-macros-recognition-openrouter.md) | [OpenRouter](https://openrouter.ai/docs) |
| Yandex Object Storage | Хранение фото еды | S3 API | backend | [ADR 0002](adr/0002-photo-storage.md) | [Документация](https://yandex.cloud/ru/docs/storage/) |
| Платёжный провайдер (с E10) | Подписка тренера | | backend | Предстоит | |
