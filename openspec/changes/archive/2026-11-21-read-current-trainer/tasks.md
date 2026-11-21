# Tasks

## 1. Backend

- [x] 1.1 Добавить `GET /api/trainers/me` по `design.md`: `TrainerDetailView`, `TrainerDetailDto`,
      `TrainerDetailService`, `TrainerDetailResponseSerializer`. Ответ содержит `first_name`, `last_name` и `photo`.
      Проверка: путь `trainers/me` объявлен в `trainers/api/urls.py`, сериализатор объявляет эти три поля.
- [x] 1.2 Покрыть тестом сценарий «Своё имя»: активный тренер с действующим токеном доступа получает свои имя и фамилию.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.3 Покрыть тестом сценарий «Чужое имя»: в ответе нет имени и фамилии другого тренера.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.4 Покрыть тестом сценарий «Телефон и пароль не отдаются»: в ответе нет телефона, пароля и статуса. Поле
      `photo` — адрес файла или `null`.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.5 Покрыть тестом сценарий «Нет входа»: запрос без Bearer получает `401` и не возвращает имя.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.6 Покрыть тестом сценарий «Токен обновления вместо токена доступа»: refresh как Bearer получает `401`.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.7 Покрыть тестом сценарий «Просроченный токен доступа»: истёкший access JWT получает `401`.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.8 Покрыть тестом сценарий «Токен без подписи кабинета»: чужой Bearer получает `401`.
      Проверка: `uv run python manage.py test` проходит.
- [x] 1.9 Покрыть тестом сценарий «Заблокированный тренер»: запрос имени после блокировки получает `401` и не возвращает
      имя. Проверка: `uv run python manage.py test` проходит.
- [x] 1.10 Описать `GET /api/trainers/me` в OpenAPI: Bearer, `first_name`, `last_name`, без телефона в этом ответе.
      Проверка: `GET /api/schema/` содержит путь, оба поля и схему Bearer.

## 2. Frontend

- [x] 2.1 Обновить снимок `frontend/api-client/openapi.json` и типы командами из README. Пакет `dashboard/` не
      создавать. Проверка: в снимке есть `/api/trainers/me`, `pnpm --filter api-client generate` завершается.

## 3. Docs

- [x] 3.1 В `docs/architecture/c4/components.md` у компонента «Тренер» указать чтение своего имени. ADR, модель данных и
      глоссарий не менять. Проверка: в описании компонента есть это чтение, новых ADR и правок `data-model.md` нет.
