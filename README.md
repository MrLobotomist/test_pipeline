# CI/CD Pipeline — Смехов П. А.

## Проект и стек

Учебный Python-проект с полным набором CI/CD-проверок на платформе GitHub Actions.

**Стек инструментов:**

| Назначение | Инструмент |
|------------|-----------|
| Язык | Python 3.11+ |
| Тестирование | pytest, pytest-cov |
| Линтер и форматирование | ruff |
| Статическая типизация | mypy |
| Анализ безопасности кода | bandit |
| Поиск секретов | trufflehog |
| Сканирование зависимостей | pip-audit |
| CI-платформа | GitHub Actions |

---

## Схема пайплайна

1. **Статический анализ (lint)** — ruff check, ruff format --check, mypy --strict.
2. **Модульные тесты (test)** — pytest с порогом покрытия 80%.
3. **Интеграционные тесты (integration)** — pytest -m integration (запускается только при слиянии в main).
4. **Сканирование безопасности (security)** — trufflehog (поиск секретов), bandit (небезопасные конструкции), pip-audit (уязвимости в зависимостях).
5. **Уведомления (notify)** — оповещение в Slack при сбое любого этапа.

---

## Правила, обеспечиваемые техническими средствами

- Прямой push в ветку main запрещён.
- Слияние возможно только через Pull Request.
- Требуется минимум 1 одобрение от ревьюера.
- Все обязательные проверки CI (lint, test, security) должны завершиться успешно.
- Стратегия слияния: Rebase and merge.
- Файл CODEOWNERS определяет автоматических ревьюеров для каждой области проекта.
- Безобвинительная культура: post-mortem по шаблону, без персонализации ошибок.

---

## Расположение файлов

```
СмеховПА/
├── pipeline_design.md         — архитектура и этапы пайплайна
├── workflow_rules.md          — правила командной работы и защиты веток
├── ci_config/
│   ├── main.yaml              — основной пайплайн (lint, test, integration, notify)
│   └── security_scans.yaml    — сканирование безопасности (trufflehog, bandit, pip-audit)
├── demo_scenarios/
│   ├── broken_build.md        — сценарий: нестабильный тест
│   └── security_incident.md   — сценарий: утечка API-ключа
└── README.md                  — данный отчёт
```

---

## Локальный запуск проверок

### Установка зависимостей

```bash
pip install ruff mypy pytest pytest-cov bandit pip-audit pre-commit
```

### Линтер и форматирование

```bash
ruff check src/
ruff format --check src/
```

### Проверка типов

```bash
mypy --strict src/
```

### Модульные тесты с покрытием

```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80 -v
```

### Сканирование безопасности

```bash
bandit -r src/
pip-audit --strict
```

### Настройка pre-commit (поиск секретов перед коммитом)

```bash
pre-commit install
```

---

## Демонстрационные сценарии

- [Нестабильный тест (Flaky Test)](demo_scenarios/broken_build.md) — разработчик отправил тест, зависящий от текущего времени; описан процесс диагностики, исправления и выводы для команды.
- [Утечка API-ключа](demo_scenarios/security_incident.md) — в коммит попал секрет; описаны автоматическое обнаружение, процедура устранения, ротация ключа и меры по предотвращению повторения.
