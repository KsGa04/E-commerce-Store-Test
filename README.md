# 🧪 E-commerce Store Test Automation

**Проект:** E-commerce-Store-Test — автоматизация тестирования интернет‑магазина (API + UI + интеграционные тесты) с продвинутой системой отчетности (Allure) и CI (GitHub Actions).

---

## 📋 Оглавление

* [Обзор проекта](#-обзор-проекта)
* [Ключевые особенности](#-ключевые-особенности)
* [Архитектура проекта](#-архитектура-проекта)
* [Технологический стек](#-технологический-стек)
* [Требования и подготовка окружения](#-требования-и-подготовка-окружения)
* [Установка](#-установка)
* [Запуск тестов](#-запуск-тестов)

  * [Через `run_tests.py`](#через-run_testspy)
  * [Прямой запуск Pytest](#прямой-запуск-pytest)
  * [Параллельный запуск](#параллельный-запуск)
* [Структура тестов](#-структура-тестов)
* [Маркировка тестов (pytest markers)](#-маркировка-тестов-pytest-markers)
* [Отчетность (Allure)](#-отчетность-allure)
* [CI/CD (GitHub Actions) — пример workflow](#-cicd-github-actions---пример-workflow)
* [Полезные команды и отладка](#-полезные-команды-и-отладка)
* [Тестовые данные](#-тестовые-данные)

---

## 🎯 Обзор проекта

Проект представляет собой полную систему автоматизированного тестирования e‑commerce приложения:

* **API тестирование** — REST API endpoints (auth, products, categories, reviews и т.д.)
* **UI тестирование** — автоматизация браузера через Playwright (Page Object Model)
* **Интеграционные тесты** — end‑to‑end сценарии, комбинирующие API + UI
* **Отчётность** — Allure отчёты с шагами, вложениями и скриншотами
* **CI/CD** — автоматический запуск тестов и сбор артефактов в GitHub Actions

---

## 🧩 Ключевые особенности

* Комплексное покрытие (API + UI + интеграции)
* 30+ тест кейсов (позитивные и негативные сценарии)
* Allure с детализированными шагами, скриншотами и логами HTTP
* Поддержка параллельного выполнения (pytest-xdist)
* Селективный запуск по маркерам
* Page Object Pattern для UI тестов

---

## 🏗️ Архитектура проекта

```
E-commerce-Store-Test/
├── config/                 # Конфигурационные файлы
├── src/api/                # API клиенты и утилиты
├── tests/
│   ├── api/                # API тесты
│   │   ├── auth/           # Тесты авторизации
│   │   ├── products/       # Тесты товаров
│   │   ├── categories/     # Тесты категорий
│   │   ├── reviews/        # Тесты отзывов
│   │   └── integration/    # Интеграционные тесты
│   └── ui/                 # UI тесты
│       ├── pages/          # Page Object Model
│       ├── tests/          # UI тест-кейсы
│       └── utils/          # Вспомогательные утилиты
├── reports/                # Allure результаты/отчёты
├── screenshots/            # Скриншоты при падениях/ключевых шагах
├── run_tests.py            # Основной скрипт запуска (CLI)
└── requirements.txt        # Зависимости
```

---

## 🛠 Технологический стек

| Технология     | Назначение                                 |
|----------------|--------------------------------------------|
| Python 3.11+   | Основной язык                              |
| Pytest         | Фреймворк тестирования                     |
| Playwright     | UI автоматизация (Chromium/Firefox/WebKit) |
| Requests       | HTTP клиент для API тестов                 |
| Allure         | Отчётность                                 |
| pytest-xdist   | Параллельный запуск                        |
| GitHub Actions | CI/CD                                      |

---

## ⚙️ Требования и подготовка окружения

**Предварительные требования:**

* Python 3.11 или выше
* Git
* Node.js (для Playwright CLI, если нужно)
* Allure (опционально для локального просмотра отчётов)

**Установка Allure (локально, опционально):**

* **Windows**: скачать бинарник и распаковать в `C:\allure\` (и добавить в PATH)
* **macOS (Homebrew)**: `brew install allure`
* **Ubuntu/Debian**: `sudo apt-get install -y allure` (или скачать release и распаковать)

---

## 🧭 Установка

```bash
# Клонируем репозиторий
git clone https://github.com/KsGa04/E-commerce-Store-Test.git
cd E-commerce-Store-Test

# Создаём виртуальное окружение
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Устанавливаем браузеры Playwright
playwright install
```

---

## 🚀 Запуск тестов

### Через `run_tests.py`

`run_tests.py` — удобный обёртка-скрипт для запуска наборов тестов.

```bash
python run_tests.py
```

Скрипт предлагает опции:

1. 🔄 Все тесты (API + UI)
2. 🔥 Smoke тесты
3. 🔐 Тесты логина
4. ⚙️ Тесты админки
5. 📊 Regression тесты
6. 🌐 Только API тесты
7. 🖥️ Только UI тесты
8. 📈 Запуск с Allure отчетом
9. ⚡ Параллельный запуск
10. 🎯 Генерация Allure отчета

> Скрипт можно запускать с флагами (если реализовано) — пример:
>
> `python run_tests.py --type api --allure --workers 4`

### Прямой запуск через Pytest

```bash
# Все тесты
pytest -v

# Только API тесты
pytest -m api -v

# Только UI тесты
pytest -m ui -v

# С генерацией Allure результатов
pytest -v --alluredir=reports/allure-results

# Только smoke
pytest -m smoke -v
```

### Параллельный запуск (pytest-xdist)

```bash
pytest -n auto -v
# или указать конкретное количество воркеров
pytest -n 4 -v
```

---

## 📊 Структура тестов (деталь)

### 🔌 API тесты

| Модуль     | Эндпоинты                       | Описание                 |
|------------|---------------------------------|--------------------------|
| Auth       | `/auth/login`, `/auth/register` | Авторизация/регистрация  |
| Products   | `/products`                     | CRUD операции с товарами |
| Categories | `/categories`                   | Работа с категориями     |
| Reviews    | `/products/{id}/review`         | Отзывы о товарах         |
| Workflows  | интеграционные                  | Сложные бизнес-сценарии  |

### 🖥️ UI тесты

**Page Objects:** `tests/ui/pages/` — классы страниц с методами действий (POM).

**Тесты:** `tests/ui/tests/` — наборы кейсов (позитив/негатив/edge cases).

---

## 🏷️ Маркировка тестов (pytest markers)

Используемые маркеры:

* `@pytest.mark.api` — API тесты
* `@pytest.mark.ui` — UI тесты
* `@pytest.mark.smoke` — Smoke тесты
* `@pytest.mark.regression` — Регрессионные тесты
* `@pytest.mark.login` — Тесты авторизации
* `@pytest.mark.admin` — Тесты админки

Добавьте в `pytest.ini` следующее, чтобы избежать предупреждений:

```ini
[pytest]
markers =
    api: API tests
    ui: UI tests
    smoke: Smoke tests
    regression: Regression tests
    login: Login tests
    admin: Admin tests
```

---

## 📈 Отчетность (Allure)

### Сбор результатов

```bash
pytest -v --alluredir=reports/allure-results
```

### Генерация HTML отчёта

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### Что автоматически прикрепляется

* Скриншоты при падении теста
* Логи HTTP (request/response) для API
* Текстовые логи и шаги теста
* Тривиальные вложения (файлы) по требованию

---

## 🔁 CI/CD — GitHub Actions (пример)

*Nиже пример workflow, который запускает тесты и сохраняет артефакты Allure результатов.*

```yaml
name: CI Tests

on:
  push:
    branches: [ master, develop, feature/** ]
  pull_request:
    branches: [ master, develop ]
  schedule:
    - cron: '0 2 * * *'  # Ежедневный запуск в 2:00 AM
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false

    steps:
      - name: Debug Info
        run: |
          echo "Event: ${{ github.event_name }}"
          echo "Ref: ${{ github.ref }}"
          echo "HEAD SHA: ${{ github.sha }}"

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest requests allure-pytest pytest-xdist

      - name: Install Playwright
        run: |
          pip install playwright
          python -m playwright install
          python -m playwright install-deps

      - name: Show directory structure
        run: |
          echo "Project structure:"
          find . -name "*.py" | head -20
          echo "Tests structure:"
          find tests -type f | head -20

      - name: Run API tests
        run: |
          python -m pytest tests/api/ -v --alluredir=reports/allure-results

      - name: Run UI tests
        run: |
          python -m pytest tests/ui/tests/ -v --alluredir=reports/allure-results
        env:
          HEADLESS: true
          PLAYWRIGHT_HEADLESS: true

      - name: Install Allure
        run: |
          sudo apt-get update
          sudo apt-get install default-jre -y
          wget -q https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
          tar -zxvf allure-2.24.1.tgz
          sudo mv allure-2.24.1 /opt/allure
          sudo ln -s /opt/allure/bin/allure /usr/bin/allure

      - name: Generate Allure report
        run: |
          mkdir -p allure-report
          allure generate reports/allure-results -o allure-report --clean

      - name: Upload Allure report
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-report
          retention-days: 30

      - name: Test Summary
        if: always()
        run: |
          echo "## 🧪 Test Results Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### 📊 Test Execution" >> $GITHUB_STEP_SUMMARY
          echo "✅ **API Tests**: Completed" >> $GITHUB_STEP_SUMMARY
          echo "✅ **UI Tests**: Completed" >> $GITHUB_STEP_SUMMARY
          echo "📁 **Allure Report**: Generated and available as artifact" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### 🔍 Next Steps" >> $GITHUB_STEP_SUMMARY
          echo "1. Download the 'allure-report' artifact from this run" >> $GITHUB_STEP_SUMMARY
          echo "2. Extract the artifact" >> $GITHUB_STEP_SUMMARY
          echo "3. Open `index.html` in your browser to view the detailed report" >> $GITHUB_STEP_SUMMARY
```

*В CI размещайте секреты (API_TOKEN и пр.) через GitHub Secrets.*

---

## 🐞 Полезные команды и отладка

```bash
# Проверка импортов
python tests/ui/utils/check_imports.py

# Проверка Allure настроек
python tests/ui/utils/check_allure.py

# Запуск с pdb при падении
pytest -v --pdb

# Запуск с подробными логами
pytest -v -s
```

---

## 🧪 Тестовые данные

* **Базовый URL:** `https://v0-swagger-backend-frontend.vercel.app`
* **Демо‑учётные данные:**

  * Логин: `admin`
  * Пароль: `admin123`

> В тестах используются фикстуры для подготовки данных (создание/удаление через API), чтобы тесты были детерминированы.

---
