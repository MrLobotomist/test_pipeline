# Сценарий: утечка API-ключа в репозиторий

## Ситуация

Разработчик реализовал интеграцию с внешним сервисом уведомлений. Для локального тестирования он вставил API-ключ непосредственно в конфигурационный файл `src/config.py` и забыл удалить его перед отправкой коммита. Pull Request содержит строку:

```python
NOTIFICATION_API_KEY = "sk-live-4f8a2b1c9d3e7f6a5b0c8d2e1f4a7b3c"
```

---

## Лог задания Security в CI

```
=== trufflehog scan results ===
Running trufflehog against git history...

Found verified secret in commit abc1234:
  Detector: GenericApiKey
  File:     src/config.py
  Line:     12
  Secret:   sk-live-4f8a2b1c...7b3c
  Verified: True

Results:
  Verified secrets found: 1
  Unverified secrets found: 0

ERROR: Verified secrets detected. Pipeline failed.

=== bandit scan results ===
Run started: 2025-01-15 14:32:10

Test results:
  >> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'sk-live-4f8a2b1c9d3e7f6a5b0c8d2e1f4a7b3c'
     Severity: Medium   Confidence: Medium
     CWE: CWE-259
     Location: src/config.py:12

  Code:
  11  class Config:
  12      NOTIFICATION_API_KEY = "sk-live-4f8a2b1c9d3e7f6a5b0c8d2e1f4a7b3c"

--------------------------------------------------
Files analyzed: 15
Issues found: 1 (severity: Medium)

=== pip-audit results ===
No known vulnerabilities found.

=== Security scan summary ===
trufflehog: FAIL (1 verified secret)
bandit:     FAIL (1 hardcoded secret)
pip-audit:  PASS

Overall: FAIL
```

---

## Автоматические действия системы

При обнаружении секрета в CI происходит следующее:

1. **Пайплайн завершается с ошибкой.** Кнопка Merge в PR становится недоступной. В интерфейсе отображается красный статус проверки `security`.

2. **Уведомление в Slack-канал команды:**

```
[CI Security Alert] PR #58: обнаружен секрет в коммите abc1234
Файл: src/config.py, строка 12
Тип: GenericApiKey (подтверждённый)
Действие: слияние заблокировано до устранения
Ответственный: @developer
```

3. **Уведомление на электронную почту автора PR** с инструкцией по устранению.

---

## Процесс исправления

### Шаг 1. Удаление секрета из кода

Разработчик заменяет жёстко заданное значение на чтение из переменной окружения:

```python
import os

NOTIFICATION_API_KEY = os.environ.get("NOTIFICATION_API_KEY", "")
```

Для удобства локальной разработки создаётся файл `.env.example` (без реальных значений):

```
NOTIFICATION_API_KEY=your-api-key-here
```

Файл `.env` добавлен в `.gitignore`.

### Шаг 2. Очистка истории Git

Поскольку секрет попал в историю коммитов, простого удаления из файла недостаточно. Используется инструмент `git filter-repo` для перезаписи истории:

```bash
git filter-repo --path src/config.py --invert-paths
```

Либо, если требуется сохранить файл но удалить строку из всей истории:

```bash
git filter-repo --replace-text expressions.txt
```

где `expressions.txt` содержит: `sk-live-4f8a2b1c9d3e7f6a5b0c8d2e1f4a7b3c==>REDACTED`.

### Шаг 3. Ротация ключа

Скомпрометированный ключ отзывается в панели управления внешнего сервиса. Генерируется новый ключ и размещается в безопасном хранилище (GitHub Secrets, Vault или аналогичное решение). Старый ключ считается скомпрометированным вне зависимости от того, был ли он реально использован третьей стороной.

### Шаг 4. Настройка локальной защиты

Для предотвращения повторных инцидентов устанавливается pre-commit хук:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.82.13
    hooks:
      - id: trufflehog
        entry: trufflehog git file://. --only-verified --fail
```

Установка:

```bash
pip install pre-commit
pre-commit install
```

Теперь при каждом локальном коммите выполняется проверка на наличие секретов. Коммит с секретом будет отклонён ещё до отправки в удалённый репозиторий.

### Шаг 5. Настройка списка исключений (при необходимости)

Если trufflehog выдаёт ложноположительное срабатывание (например, на тестовый токен или пример из документации), допускается добавление исключения:

```yaml
# .trufflehog-ignore
# Тестовый токен для модульных тестов (не является реальным секретом)
abc123-test-token-not-real
```

Исключения добавляются только после подтверждения ложноположительного срабатывания двумя участниками команды.

---

## Хронология инцидента (Post-mortem)

| Время | Событие |
|-------|---------|
| 14:25 | Разработчик отправил коммит с API-ключом в PR #58 |
| 14:32 | CI обнаружил секрет, пайплайн завершился с ошибкой |
| 14:33 | Автоматическое уведомление в Slack и на почту |
| 14:40 | Разработчик начал устранение проблемы |
| 14:55 | Секрет удалён из кода, история перезаписана |
| 15:10 | Старый ключ отозван, новый размещён в GitHub Secrets |
| 15:20 | Повторный запуск CI: все проверки пройдены |
| 15:30 | Настроен pre-commit хук для всей команды |

**Время от утечки до обнаружения:** 7 минут (автоматически).
**Время до полного устранения:** 55 минут.

---

## Меры по предотвращению повторения

1. Pre-commit хук с trufflehog установлен у всех участников команды.
2. В документацию по онбордингу добавлена инструкция по настройке pre-commit.
3. Все конфиденциальные значения хранятся исключительно в GitHub Secrets и передаются через переменные окружения.
4. Файлы `.env` добавлены в `.gitignore` на уровне репозитория.
5. Проведено обучение команды по безопасной работе с секретами.
