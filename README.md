# Trenly

Trenly — сервис для персональных фитнес-тренеров и их клиентов. Клиент работает через Telegram-бота, тренер — через веб-кабинет.

Всё в одном репозитории: документация, спецификации [OpenSpec](https://github.com/Fission-AI/OpenSpec), бэкенд и фронтенд ([ADR 0003](docs/architecture/adr/0003-monorepo.md)).

## Структура

```text
trenly-ai/
├── docs/          бизнес-требования, архитектура, нефункциональные требования
├── openspec/      функциональные требования и изменения в работе
├── backend/       API кабинета тренера, Telegram-бот, интеграции (появится в E1)
├── frontend/      веб-кабинет тренера (появится в E1)
├── templates/     шаблоны документов
└── AGENTS.md      правила для ИИ-агентов
```

## Документация

| Раздел | Что внутри |
|---|---|
| [`docs/glossary.md`](docs/glossary.md) | Глоссарий терминов |
| [`docs/spec-driven-process.md`](docs/spec-driven-process.md) | Как ведётся разработка по спецификациям |
| [`docs/business`](docs/business) | Видение, бизнес-требования (BR), метрики, роадмап |
| [`docs/architecture`](docs/architecture) | C4-модель, ADR, интеграции |
| [`docs/nfr`](docs/nfr) | Нефункциональные требования: безопасность, персональные данные, производительность |
| [`docs/api`](docs/api) | API-контракты и правила их версионирования |
| [`docs/operations`](docs/operations) | Окружения, релизный процесс, runbooks |
| [`openspec`](openspec) | Функциональные требования: спецификации и изменения |

## Как связаны документы

```text
Бизнес-требование (BR-xxx)       docs/business/requirements.md
        │  «зачем»
        ▼
Функциональные требования         openspec/specs/<capability>/spec.md
        │  «что делает система для тренера и клиента»
        ▼
Изменение                         openspec/changes/<change-id>/
        │  «как реализуем: design.md, tasks.md»
        ▼
Код                               backend/, frontend/
```
