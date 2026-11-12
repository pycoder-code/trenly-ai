# Tasks

## 1. Docs: номер ADR

- [x] 1.1 Переименовать `docs/architecture/adr/0007-client-mini-app.md` в `0008-client-mini-app.md`. Обновить реестр ADR, ссылку из ADR 0006 и `docs/architecture/c4/containers.md`. Ссылку `docs/nfr/security.md` на `0007-trainer-is-not-django-user.md` не менять. Проверка: в реестре один ADR 0007 и один ADR 0008, поиск по репозиторию не находит `0007-client-mini-app`.

## 2. Frontend: workspace и клиент API

- [x] 2.1 Создать pnpm workspace в `frontend/` с пакетами `miniapp/` и `api-client/`. Пакет `dashboard/` не создавать. В корневой `.gitignore` добавить `node_modules/` и каталоги сборки. Проверка: в `frontend/` команда `pnpm install` завершается, на месте два каталога пакетов и нет `dashboard/`.
- [x] 2.2 Снять схему командой `uv run python manage.py spectacular --file ../frontend/api-client/openapi.json` из `backend/` и сгенерировать типы `openapi-typescript` для `openapi-fetch`. Закоммитить снимок и типы, описать команду регенерации так, чтобы её вызвала задача 4.1. Проверка: в `openapi.json` есть `/api/trainer-sessions` и `/api/clients`, пакет `api-client` собирается. Mini App этот пакет не импортирует.

## 3. Frontend: Mini App

- [x] 3.1 Собрать оболочку `miniapp/` на Vue 3, Vite, vue-router, `@tma.js/sdk` и `@tma.js/sdk-vue`. Экран — заглушка на цвете темы Telegram, без вызова Django и без токена. Вне Telegram страница не падает и показывает ту же заглушку. Проверка: `pnpm --filter miniapp build` завершается.

## 4. Docs: запуск

- [x] 4.1 В `README.md` заменить строку про будущий `frontend/` деревом `miniapp/` и `api-client/` и командами установки, генерации клиента и запуска Mini App. Кабинет в этих командах не упоминать. Проверка: команды из README совпадают с теми, которыми собираются пакеты в задачах 2.2 и 3.1.

## 5. Backend

Задач нет: пути API не меняются. Схему для клиента снимает задача 2.2.

## 6. Telegram-бот

Задач нет: оболочка Mini App бота не вызывает.

## Workflow follow-up

- После ревью заархивировать изменение, когда оболочка Mini App попадёт в prod.
