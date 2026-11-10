# Tasks

## 1. Backend

- [x] 1.1 Завести в `backend/` проект uv: `pyproject.toml`, `uv.lock`, `.python-version`. Зависимости — актуальные стабильные и взаимно совместимые Django, djangorestframework, drf-spectacular и драйвер PostgreSQL (psycopg). Интерпретатор — самая новая стабильная ветка Python из пересечения их поддержки. Проверка: `uv sync` в `backend/` завершается без ошибок, импорт трёх библиотек из `uv run` печатает их версии.
- [x] 1.2 Создать проект Django в пакете `config`: настройки из переменных окружения, `.env.example`, подключение PostgreSQL, DRF, drf-spectacular, Django Admin по `/admin/` и пустая схема `GET /api/schema/`. Проверка: `uv run python manage.py check` завершается без ошибок.
- [x] 1.3 Добавить в корневой `compose.yaml` сервис PostgreSQL и применить миграции Django к этой базе. Проверка: база поднимается одной командой Compose, `uv run python manage.py migrate` завершается успешно.
- [x] 1.4 Добавить `GET /api/health/` с телом `{"status": "ok"}` и тест Django на `/api/health/` и `/api/schema/`. Проверка: `uv run python manage.py test` проходит.

## 2. Docs

- [x] 2.1 Дополнить корневой `.gitignore` правилами Python, uv и локальных `.env`. В README заменить пометку «появится в E1» у `backend/` на команды: поднять PostgreSQL, применить миграции, запустить приложение. Проверка: по командам из README `GET /api/health/` возвращает `{"status": "ok"}`, а `GET /api/schema/` — документ OpenAPI.
