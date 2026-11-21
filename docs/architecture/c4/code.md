# Уровень 4. Код

Классы и структуры данных компонентов из [уровня 3](components.md). Описываются только ключевые и сложные места:
остальное видно в коде и быстро устаревает в документации.

## Тренер

Сценарий входа. `TrainerEntity` проверяет пароль. Модель `Trainer` хранит строку и правил не содержит.

```mermaid
classDiagram
    class TrainerAuthDto {
        phone
        password
    }
    class TokenPairEntity {
        access_token
        refresh_token
    }
    class TrainerEntity {
        check_password()
        is_active
    }
    class TrainerModel["Trainer (models)"] {
        phone
        password
        status
    }
    class TrainerRepository {
        get_by_phone()
    }
    class RefreshTokenRepository {
        add()
        take()
    }

    TrainerAuthDto --> TrainerRepository
    TrainerRepository --> TrainerEntity
    TrainerRepository --> TrainerModel
    TrainerEntity --> TokenPairEntity
    RefreshTokenRepository --> TokenPairEntity
```
