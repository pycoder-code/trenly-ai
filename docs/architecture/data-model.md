# Модель данных

Логическая схема доменных таблиц PostgreSQL. Диаграмма — источник правды по составу сущностей, полей и связей: любое изменение постоянных моделей обновляет этот файл в том же изменении.

Имена сущностей совпадают с колонкой «В коде» в [глоссарии](../glossary.md). Таблицы Django (`auth`, `admin`, `sessions`, `contenttypes`) здесь не показаны.

## Соглашения

Рост (`height`) хранится в сантиметрах, вес (`weight`) — в килограммах. Единицы измерения в имена полей не входят.

```mermaid
erDiagram
    Trainer ||--o{ Client : trainer
    Trainer {
        bigint id PK
        string phone UK
        string password
        string first_name
        string last_name
        string photo "пусто или ключ объекта"
        string status "active или blocked"
        timestamptz created_at
        timestamptz updated_at
    }
    Client {
        bigint id PK
        bigint trainer_id FK
        bigint telegram_user_id UK
        string telegram_username "может быть пустым"
        string first_name
        string last_name "может быть пустым"
        string phone "может быть пустым"
        int height "может быть пустым, см"
        decimal weight "может быть пустым, кг"
        string status "active или disconnected"
        timestamptz created_at
        timestamptz updated_at
    }
```
