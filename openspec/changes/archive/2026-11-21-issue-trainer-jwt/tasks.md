# Tasks

## 1. Backend

- [x] 1.1 Добавить зависимость PyJWT в `backend/`. Проверка: `uv sync` завершается, импорт `jwt` из `uv run` печатает
      версию.
- [x] 1.2 Добавить модель `RefreshToken` по `design.md`: тренер, хеш секрета, срок. Сырой секрет в базе не хранится.
      Обновить `docs/architecture/data-model.md`. Проверка: миграция применяется, на диаграмме есть `RefreshToken` и
      связь с `Trainer`.
- [x] 1.3 Заменить выпуск токена кабинета на пару по `design.md`: access JWT на 15 минут, refresh на 14 дней,
      `POST /api/access-tokens` и `POST /api/refresh-tokens`. Поле `token` убрать. Текст `401` не менять.
      Проверка: сценарии ниже проходят одним запуском `uv run python manage.py test`.
- [x] 1.4 Покрыть тестом успешный вход: `201`, `access_token` открывает `GET /api/clients`, `refresh_token` как Bearer
      получает отказ. Проверка: `uv run python manage.py test` проходит.
- [x] 1.5 Покрыть тестами отказ при неверном пароле и вход с номером, записанным с ведущей `8`: во втором случае снова
      пара токенов. Проверка: `uv run python manage.py test` проходит.
- [x] 1.6 Покрыть тестами отказ для Bearer без подписи кабинета, включая прежнюю подписанную Django-строку, и для
      просроченного access JWT. Проверка: `uv run python manage.py test` проходит.
- [x] 1.7 Покрыть тестами обмен refresh: новая пара, старый refresh больше не действует, просроченный и неизвестный
      refresh получают отказ. Проверка: `uv run python manage.py test` проходит.
- [x] 1.8 Покрыть тестами блокировку: верный пароль не выдаёт пару, уже выданный access JWT получает отказ на следующем
      запросе, refresh заблокированного тренера новую пару не выдаёт. Проверка: `uv run python manage.py test` проходит.
- [x] 1.9 Смена пароля и сохранение тренера в админке не удаляют `RefreshToken`. Отдельного теста на смену пароля нет.

## 2. Backend: OpenAPI

- [x] 2.1 Описать `access_token`, `refresh_token` и `POST /api/refresh-tokens`. Схему Bearer оставить.
      Проверка: `GET /api/schema/` содержит оба пути, `/api/clients`, схему Bearer и не содержит поля `token` у входа.

## 3. Frontend

- [x] 3.1 Обновить снимок `frontend/api-client/openapi.json` и типы командами из README. Пакет `dashboard/` не
      создавать. Проверка: в снимке есть `access_token` и `refresh_token`, `pnpm --filter api-client generate`
      завершается.

## 4. Docs

- [x] 4.1 В ADR 0010 указать изменение `issue-trainer-jwt`. Роадмап не менять. Проверка: в ADR есть идентификатор
      изменения.

## 5. Telegram-бот

Задач нет: бот эту пару не выпускает и не проверяет.

## Workflow follow-up

- После ревью заархивировать изменение, когда пара токенов кабинета попадёт в prod.
