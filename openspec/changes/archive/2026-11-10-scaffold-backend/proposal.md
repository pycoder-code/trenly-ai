# Proposal

## Why

Папка `backend/` пустая, а эпик E1 начинается с каркаса API. Без установленного Django-приложения и локальной базы нельзя переходить к аккаунту тренера (E2) и к контракту OpenAPI, от которого зависит кабинет.

Бизнес-требования это изменение не закрывает: в [роадмапе](../../../docs/business/roadmap.md) у E1 колонка BR пустая.

## What Changes

- В `backend/` появляется приложение на Python, Django, Django REST Framework и drf-spectacular ([ADR 0005](../../../docs/architecture/adr/0005-tech-stack.md)).
- Локальный PostgreSQL поднимается одной командой Docker Compose из корня репозитория ([ADR 0003](../../../docs/architecture/adr/0003-monorepo.md)).
- Приложение отдаёт пустую OpenAPI-схему и страницу Django Admin. Доменных моделей, входа тренера и бота нет.
- В README появляются команды локального запуска.

## Capabilities

### New Capabilities

Нет. Для тренера, клиента и администратора поведение не меняется: это каркас приложения, а не функция продукта. Спецификации не добавляются (`skip_specs: true`).

### Modified Capabilities

Нет.

## Impact

- `backend/` — зависимости, проект Django, настройки, проверка живости API.
- `compose.yaml` в корне — сервис PostgreSQL.
- `README.md`, `.gitignore`.
- `frontend/` и `tg_bot/` не меняются. CI, деплой, S3, логирование и мониторинг остаются следующими изменениями E1.
