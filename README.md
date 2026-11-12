# Trenly

Trenly — сервис, который упрощает работу персонального фитнес-тренера с клиентами.

- **Клиент** работает через Telegram-бота: заполняет анкету, ведёт дневник питания (фото еды с оценкой КБЖУ или ручной ввод), отмечает тренировки, получает рекомендации по питанию и награды за регулярность.
- **Тренер** работает в веб-кабинете: видит всех своих клиентов, их прогресс, журнал и отчёты, получает уведомления (например, что клиент не придёт на тренировку).
- **Администратор** управляет тренерами через админку: на старте добавляет их вручную.

Для тренера сервис платный (ежемесячная подписка после пилота), для клиента — бесплатный. Пользователи находятся в России.

Подробнее — в [видении продукта](docs/business/vision.md).

## Как ведётся разработка

Разработка ведётся по спецификациям с помощью [OpenSpec](https://github.com/Fission-AI/OpenSpec): сначала согласуются требования, затем ИИ-агент и разработчики реализуют их по задачам.

```text
/opsx:propose <change-id>   предложение: требования, дизайн, задачи
/opsx:apply                 реализация по задачам
/opsx:archive               после выкатки требования попадают в openspec/specs/
```

Процесс целиком — в [docs/spec-driven-process.md](docs/spec-driven-process.md), правила для ИИ-агентов — в [AGENTS.md](AGENTS.md).

## Технологии

| Часть | Технологии |
|---|---|
| Бэкенд (API, админка, интеграции) | Python, Django, Django REST Framework, drf-spectacular ([ADR 0005](docs/architecture/adr/0005-tech-stack.md)) |
| Telegram-бот | aiogram 3, отдельное приложение, связь с API по HTTP ([ADR 0006](docs/architecture/adr/0006-telegram-bot-aiogram.md)) |
| База данных | PostgreSQL ([ADR 0005](docs/architecture/adr/0005-tech-stack.md)) |
| Состояния диалога бота | Redis ([ADR 0006](docs/architecture/adr/0006-telegram-bot-aiogram.md)) |
| Админка | Django Admin ([ADR 0005](docs/architecture/adr/0005-tech-stack.md)) |
| Кабинет тренера | Vue 3, TypeScript, Vite, PrimeVue, Pinia ([ADR 0005](docs/architecture/adr/0005-tech-stack.md)) |
| Хранение фото | Yandex Object Storage ([ADR 0002](docs/architecture/adr/0002-photo-storage.md)) |
| Распознавание КБЖУ | OpenRouter, модель Gemini 3.8 Flash ([ADR 0004](docs/architecture/adr/0004-macros-recognition-openrouter.md)) |
| Канал клиента | Telegram Bot API |

## Структура репозитория

Монорепозиторий ([ADR 0003](docs/architecture/adr/0003-monorepo.md)):

```text
trenly-ai/
├── docs/          документация
├── openspec/      функциональные требования и изменения в работе
├── backend/       Django: API, интеграции, админка
├── frontend/      Vue: оболочка Mini App и клиент API
│   ├── api-client/  типы и fetch по схеме OpenAPI
│   └── miniapp/     оболочка Mini App
├── tg_bot/        aiogram 3: чат клиента (зависимости; диалоги — E3, ADR 0006)
├── templates/     шаблоны документов
└── AGENTS.md      правила для ИИ-агентов
```

## Локальный запуск бэкенда

Нужны [uv](https://docs.astral.sh/uv/) и Docker Compose. Compose поднимает PostgreSQL для API и Redis для незавершённого шага чата бота. Django к Redis не подключается: состояния диалога читает и пишет только `tg_bot/` ([ADR 0006](docs/architecture/adr/0006-telegram-bot-aiogram.md)). Из корня:

```bash
docker-compose up -d
cp backend/.env.example backend/.env
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Если установлен плагин Compose V2, хранилища поднимает `docker compose up -d`. Redis слушает `localhost:6379` без пароля — только для локального запуска.

Приложение слушает http://127.0.0.1:8000. `GET /api/health/` возвращает `{"status": "ok"}`, `GET /api/schema/` — документ OpenAPI. Админка: http://127.0.0.1:8000/admin/.

Зависимости бота ставятся отдельно, тем же интерпретатором Python 3.14:

```bash
cd tg_bot
uv sync
```

Прямая зависимость — `aiogram[redis]` 3.31: фреймворк бота и клиент Redis для шага диалога. Вызовы внутреннего API Django появятся вместе с кодом бота.

## Локальный запуск Mini App

Нужны Node.js и pnpm 12. Если команда `pnpm` не находится, один раз включите её через Corepack, он идёт вместе с Node: `corepack enable`. Из корня:

```bash
cd frontend
pnpm install
```

Клиент API генерируется из схемы Django. Схему снимают из `backend/`, типы — из `frontend/`:

```bash
cd backend
uv run python manage.py spectacular --file ../frontend/api-client/openapi.json --format openapi-json
cd ../frontend
pnpm --filter api-client generate
```

Запуск оболочки:

```bash
cd frontend
pnpm --filter miniapp dev
```

Сборка оболочки:

```bash
cd frontend
pnpm --filter miniapp build
```

## Документация

| Документ | Что внутри |
|---|---|
| [Видение](docs/business/vision.md) | Суть продукта, роли, цели, границы |
| [Бизнес-требования](docs/business/requirements.md) | BR-001…BR-011: зачем нужна каждая функция |
| [Роадмап](docs/business/roadmap.md) | Эпики и порядок реализации |
| [Метрики](docs/business/metrics.md) | Как понять, что продукт работает |
| [Глоссарий](docs/glossary.md) | Термины и имена сущностей в коде |
| [Функциональные требования](openspec/specs) | Спецификации OpenSpec |
| [C4-модель](docs/architecture/c4/README.md) | Архитектура: контекст, контейнеры, компоненты, код |
| [Модель данных](docs/architecture/data-model.md) | Логическая схема PostgreSQL, диаграмма `erDiagram` |
| [ADR](docs/architecture/adr/README.md) | Архитектурные решения |
| [Интеграции](docs/architecture/integrations.md) | Внешние системы |
| [Нефункциональные требования](docs/nfr) | Безопасность, персональные данные, производительность |
| [API](docs/api/README.md) | API-контракты |
| [Эксплуатация](docs/operations) | Окружения, релизы, runbooks |

## Как связаны документы

```text
Бизнес-требование (BR-xxx)       docs/business/requirements.md
        │  «зачем»
        ▼
Функциональные требования         openspec/specs/<capability>/spec.md
        │  «что делает система»
        ▼
Изменение                         openspec/changes/<change-id>/
        │  «как реализуем: design.md, tasks.md»
        ▼
Код                               backend/, frontend/, tg_bot/
```
