---
name: commit
description:
  Коммитит доработку OpenSpec на ветке feature/<change-id> и открывает pull request в main. Use when the user says "opsx
  commit", "скилл commit", "закоммить и создай MR", "commit и MR в main", or asks to commit a finished OpenSpec change
  and open a merge request into the main branch.
---

# Commit

Коммит готовой доработки и pull request в `main`. Ветку этот скилл не создаёт: `feature/<change-id>` уже есть до
`/opsx:apply`.

На GitHub merge request — это pull request. База — `main`.

## Остановиться

- Текущая ветка — `main` или имя не `feature/<change-id>`. Не коммитить и не пушить. Назвать нужную ветку.
- Нечего коммитить и нет коммитов поверх `main`. Пустой коммит не создавать.
- В изменениях секреты (`.env`, ключи, `credentials`). Не добавлять их в коммит и сказать об этом.

Не менять git config. Не делать `--no-verify`, `--no-gpg-sign`, force push и push в `main`. Не мержить pull request.

## Шаги

1. Имя изменения — аргумент пользователя или единственное активное из `openspec list --json`. Если активных несколько,
   спросить. `<change-id>` — идентификатор изменения, например `add-nutrition-diary`.
2. Проверить ветку: `git branch --show-current`. Ожидается `feature/<change-id>`.
3. Параллельно снять состояние:

   ```bash
   git status
   git diff
   git diff --staged
   git log -8 --oneline
   ```

4. Если есть незакоммиченные изменения, собрать коммит. `git add` — только файлы этой доработки. Сообщение по-русски,
   одно-два предложения, зачем изменение, в стиле коротких сообщений репозитория. Передать его через HEREDOC:

   ```bash
   git commit -m "$(cat <<'EOF'
   Зачем эта доработка.

   EOF
   )"
   ```

   Хук отклонил коммит или сам поправил файлы — исправить и сделать новый коммит. `--amend` только если коммит создан в
   этом же запуске, хук лишь дописал файлы, и ветка ещё не на remote.

5. `git status` после коммита.
6. `git push -u origin HEAD`.
7. Если pull request этой ветки уже есть, вернуть его URL:

   ```bash
   gh pr view --json url --jq .url
   ```

   Иначе создать pull request в `main` и вернуть URL:

   ```bash
   gh pr create --base main --title "краткое название" --body "$(cat <<'EOF'
   ## Summary
   - зачем доработка

   ## Test plan
   - [ ] что проверить

   EOF
   )"
   ```

В ответе пользователю дать URL pull request.
