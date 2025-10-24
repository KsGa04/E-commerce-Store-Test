#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil

# Фиксированный путь к Allure
ALLURE_PATH = r"C:\allure\allure-2.35.1\bin\allure.bat"


def check_allure_installed():
    """Проверка установлен ли Allure"""
    if os.path.exists(ALLURE_PATH):
        try:
            result = subprocess.run([ALLURE_PATH, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Allure найден: {ALLURE_PATH}")
                print(f"✅ Версия: {result.stdout.strip()}")
                return ALLURE_PATH
        except Exception as e:
            print(f"❌ Ошибка при проверке Allure: {e}")

    print("❌ Allure не найден или не работает")
    print(f"   Ожидаемый путь: {ALLURE_PATH}")
    return None


def run_tests():
    """Запуск тестов с разными опциями"""

    # Получаем корневую директорию проекта
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Определяем пути для отчетов
    allure_results_dir = os.path.join(project_root, "reports", "allure-results")
    allure_report_dir = os.path.join(project_root, "reports", "allure-report")

    # Проверяем Allure
    allure_path = check_allure_installed()
    allure_installed = allure_path is not None

    commands = {
        "1": ["pytest", "-v"],  # Все тесты
        "2": ["pytest", "-m", "smoke", "-v"],  # Smoke тесты
        "3": ["pytest", "-m", "login", "-v"],  # Тесты логина
        "4": ["pytest", "-m", "admin", "-v"],  # Тесты админки
        "5": ["pytest", "-m", "regression", "-v"],  # Regression тесты
        "6": ["pytest", "-m", "api", "-v"],  # Только API тесты
        "7": ["pytest", "-m", "ui", "-v"],  # Только UI тесты
        "8": ["pytest", "-v", "--alluredir", allure_results_dir],  # С Allure отчетом
        "9": ["pytest", "-n", "auto", "-v", "--alluredir", allure_results_dir],  # Параллельный запуск
    }

    print("=" * 60)
    print("🚀 СИСТЕМА ЗАПУСКА ТЕСТОВ")
    print("=" * 60)
    print("✅ Настройки pytest.ini:")
    print(f"   - testpaths: tests")
    print(f"   - allure-results: {allure_results_dir}")
    print(f"   - Запуск всех тестов: API + UI")
    print("=" * 60)

    if allure_installed:
        print("✅ Allure готов к работе!")
    else:
        print("⚠️  Allure не доступен. Отчеты будут генерироваться без Allure.")
    print("=" * 60)

    print("Выберите вариант запуска:")
    print("1 - 🔄 Все тесты (API + UI)")
    print("2 - 🔥 Smoke тесты")
    print("3 - 🔐 Тесты логина")
    print("4 - ⚙️  Тесты админки")
    print("5 - 📊 Regression тесты")
    print("6 - 🌐 Только API тесты")
    print("7 - 🖥️  Только UI тесты")
    print("8 - 📈 Запуск с генерацией Allure отчетов")
    print("9 - ⚡ Параллельный запуск всех тестов")
    print("0 - 🎯 Только генерация Allure отчета")
    print("=" * 60)

    choice = input("Введите номер (0-9): ").strip()

    if choice == "0":
        if not allure_installed:
            print("❌ Allure не установлен. Сначала установите Allure.")
            sys.exit(1)
        print("🎯 Генерация Allure отчета из существующих результатов")
        generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)
        return

    if choice not in commands:
        print("❌ Неверный выбор")
        sys.exit(1)

    command = commands[choice].copy()

    # Добавляем Allure ко всем командам если выбран не Allure-специфичный вариант
    if choice in ["1", "2", "3", "4", "5", "6", "7"] and allure_installed:
        command.extend(["--alluredir", allure_results_dir])

    print(f"🔄 Запуск: {' '.join(command)}")
    print("=" * 60)

    # Устанавливаем рабочую директорию в корень проекта
    os.chdir(project_root)

    # Создаем директории для отчетов
    os.makedirs(allure_results_dir, exist_ok=True)
    os.makedirs(allure_report_dir, exist_ok=True)

    # Запускаем тесты
    result = subprocess.run(command)

    # Предлагаем открыть отчет после завершения
    if allure_installed and result.returncode in [0, 1]:
        open_report = input("\n📊 Хотите открыть Allure отчет? (y/n): ").strip().lower()
        if open_report == 'y':
            generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)
    elif not allure_installed:
        print("\n📊 Allure не установлен. Отчет не может быть сгенерирован.")

    sys.exit(result.returncode)


def generate_and_open_report(allure_path, results_dir, report_dir):
    """Генерация и открытие Allure отчета"""
    print("\n📊 Генерация Allure отчета...")

    # Проверяем есть ли результаты тестов
    if not os.path.exists(results_dir):
        print(f"❌ Директория с результатами не найдена: {results_dir}")
        print("   Сначала запустите тесты с опцией Allure")
        return

    if not os.listdir(results_dir):
        print(f"❌ Нет результатов тестов в директории: {results_dir}")
        print("   Сначала запустите тесты с опцией Allure")
        return

    print(f"📁 Результаты тестов: {results_dir}")
    print(f"📁 Будут сохранены в: {report_dir}")

    # Генерируем отчет
    generate_cmd = [
        allure_path, "generate",
        results_dir,
        "-o", report_dir,
        "--clean"
    ]

    print(f"🔧 Команда: {' '.join(generate_cmd)}")

    result = subprocess.run(generate_cmd)

    if result.returncode == 0:
        print("✅ Allure отчет успешно сгенерирован!")

        # Открываем отчет
        print("🌐 Открытие Allure отчета в браузере...")
        open_cmd = [allure_path, "open", report_dir]
        subprocess.run(open_cmd)
    else:
        print("❌ Ошибка при генерации Allure отчета")
        print("Попробуйте запустить вручную:")
        print(f'"{allure_path}" generate "{results_dir}" -o "{report_dir}" --clean')
        sys.exit(1)


if __name__ == "__main__":
    run_tests()