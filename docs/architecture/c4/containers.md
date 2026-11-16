# Уровень 2. Контейнеры

Из каких отдельно запускаемых приложений и хранилищ состоит Trenly и как они связаны. Внешние системы и пользователи —
из [контекста](context.md).

Решение по боту — [ADR 0006](../adr/0006-telegram-bot-aiogram.md). Mini App — отдельный HTTP-клиент API Django, решение
— [ADR 0008](../adr/0008-client-mini-app.md). Внешний вид кабинета и Mini App задаётся макетом в Figma
([ADR 0009](../adr/0009-ui-design-figma.md)); Figma не контейнер Trenly и в рантайме не вызывается.

## Контейнеры

- **Контейнер:** API. **Назначение:** Домен, API кабинета тренера, API Mini App и внутренний API бота, админка.
  **Технологии:** Python, Django, Django REST Framework. **Папка:** `backend/`
- **Контейнер:** Кабинет тренера. **Назначение:** Веб-интерфейс тренера в браузере. **Технологии:** Vue 3, TypeScript,
  PrimeVue. **Папка:** `frontend/dashboard/`
- **Контейнер:** Mini App. **Назначение:** Веб-интерфейс клиента внутри Telegram. **Технологии:** Vue 3, TypeScript.
  **Папка:** `frontend/miniapp/`
- **Контейнер:** Бот. **Назначение:** Чат клиента: приём апдейтов Telegram и отправка сообщений. **Технологии:** aiogram
  3, aiogram_dialog 2. **Папка:** `tg_bot/`
- **Контейнер:** База данных. **Назначение:** Клиенты, анкеты, дневник, тренировки. **Технологии:** PostgreSQL.
  **Папка:** —
- **Контейнер:** Состояния диалога. **Назначение:** Шаг диалога и черновик незавершённой пачки. **Технологии:** Redis.
  **Папка:** —

## Связи

- **Откуда:** Кабинет тренера. **Куда:** API. **Что передаётся:** Действия тренера и чтение данных клиентов.
  **Протокол:** HTTPS, JSON, Bearer
- **Откуда:** Mini App. **Куда:** API. **Что передаётся:** Дневник и итог КБЖУ, ручной ввод КБЖУ, тренировки по дням,
  статистика посещений. **Протокол:** HTTPS, JSON, Bearer
- **Откуда:** Mini App. **Куда:** Бот. **Что передаётся:** `initData` в обмен на токен клиента. Данные экранов бот не
  проксирует. **Протокол:** HTTPS, JSON
- **Откуда:** Бот. **Куда:** API. **Что передаётся:** Действие клиента (`telegram_user_id`), ключ фото еды, выдача
  токена клиента и запрос исходящих сообщений. **Протокол:** HTTP, JSON, сервисный токен
- **Откуда:** Telegram. **Куда:** Бот. **Что передаётся:** Апдейт чата. Локально бот забирает сам (polling), в
  окружениях Telegram вызывает webhook. **Протокол:** Bot API
- **Откуда:** Бот. **Куда:** Telegram. **Что передаётся:** Текст и кнопки клиенту. **Протокол:** Bot API
- **Откуда:** Бот. **Куда:** Состояния диалога. **Что передаётся:** Шаг диалога и черновик пачки. **Протокол:** Redis
- **Откуда:** API. **Куда:** База данных. **Что передаётся:** Доменные записи. **Протокол:** SQL
- **Откуда:** API. **Куда:** OpenRouter. **Что передаётся:** Фото еды и запрос оценки КБЖУ, с E3. **Протокол:** HTTPS
- **Откуда:** Бот. **Куда:** Yandex Object Storage. **Что передаётся:** Сжатое фото еды, с E3. **Протокол:** S3 API
- **Откуда:** API. **Куда:** Yandex Object Storage. **Что передаётся:** Чтение фото для распознавания и подпись ссылок
  кабинету, с E3. **Протокол:** S3 API

## Диаграмма

```mermaid
flowchart TB
    trainer["<b>Тренер</b><br/>[Пользователь]"]
    client["<b>Клиент</b><br/>[Пользователь]"]

    dashboard["<b>Кабинет тренера</b><br/>[Контейнер]<br/>Vue 3, браузер"]
    miniapp["<b>Mini App</b><br/>[Контейнер]<br/>Vue 3, WebView"]
    api["<b>API</b><br/>[Контейнер]<br/>Django, DRF"]
    bot["<b>Бот</b><br/>[Контейнер]<br/>aiogram 3, aiogram_dialog 2"]

    db["<b>База данных</b><br/>[Хранилище]<br/>PostgreSQL"]
    redis["<b>Состояния диалога</b><br/>[Хранилище]<br/>Redis"]
    photos["<b>Фото еды</b><br/>[Хранилище]<br/>Yandex Object Storage"]

    telegram["<b>Telegram</b><br/>[Внешняя система]"]

    trainer -- "Браузер" --> dashboard
    client -- "WebView" --> miniapp
    client -- "Чат" --> telegram
    dashboard -- "HTTPS, Bearer" --> api
    miniapp -- "HTTPS, Bearer" --> api
    miniapp -- "initData" --> bot
    telegram -- "Webhook или polling" --> bot
    bot -- "HTTP, сервисный токен" --> api
    bot -- "Bot API" --> telegram
    bot -- "Шаг и черновик пачки" --> redis
    bot -- "S3, загрузка JPEG" --> photos
    api -- "SQL" --> db
    api -- "S3, чтение и подпись" --> photos

    classDef person fill:#08427b,stroke:#052e56,color:#fff
    classDef container fill:#1168bd,stroke:#0b4884,color:#fff
    classDef store fill:#2e7d32,stroke:#1b5e20,color:#fff
    classDef external fill:#999,stroke:#6b6b6b,color:#fff
    class trainer,client person
    class dashboard,miniapp,api,bot container
    class db,redis,photos store
    class telegram external
```
