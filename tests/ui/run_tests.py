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

    # Получаем абсолютный путь к директории с тестами
    current_dir = os.path.dirname(__file__)
    tests_dir = os.path.join(current_dir, "tests")

    # Определяем пути для отчетов
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    allure_results_dir = os.path.join(project_root, "reports", "allure-results")
    allure_report_dir = os.path.join(project_root, "reports", "allure-report")

    # Проверяем Allure
    allure_path = check_allure_installed()
    allure_installed = allure_path is not None

    commands = [
        # Запуск всех тестов
        ["pytest", tests_dir, "-v"],

        # Запуск smoke тестов
        ["pytest", tests_dir, "-m", "smoke", "-v"],

        # Запуск тестов логина
        ["pytest", tests_dir, "-m", "login", "-v"],

        # Запуск тестов админки
        ["pytest", tests_dir, "-m", "admin", "-v"],

        # Запуск regression тестов
        ["pytest", tests_dir, "-m", "regression", "-v"],

        # Запуск с генерацией Allure отчетов
        ["pytest", tests_dir, "-v", "--alluredir", allure_results_dir, "--clean-alluredir"],

        # Параллельный запуск всех тестов
        ["pytest", tests_dir, "-n", "auto", "-v", "--alluredir", allure_results_dir],
    ]

    print("=" * 60)
    print("🚀 СИСТЕМА ЗАПУСКА ТЕСТОВ")
    print("=" * 60)

    if allure_installed:
        print("✅ Allure готов к работе!")
    else:
        print("⚠️  Allure не доступен. Отчеты будут генерироваться без Allure.")
    print("=" * 60)

    print("Выберите вариант запуска:")
    print("1 - 🔄 Все тесты")
    print("2 - 🔥 Smoke тесты (основная функциональность)")
    print("3 - 🔐 Тесты логина")
    print("4 - ⚙️  Тесты админки")
    print("5 - 📊 Regression тесты")
    print("6 - 📈 Запуск с генерацией Allure отчетов")
    print("7 - ⚡ Параллельный запуск всех тестов")
    print("8 - 🎯 Только генерация Allure отчета")
    print("=" * 60)

    choice = input("Введите номер (1-8): ").strip()

    if choice in ["1", "2", "3", "4", "5"]:
        command_index = int(choice) - 1
        command = commands[command_index]

        # Добавляем Allure если установлен
        if allure_installed:
            command.extend(["--alluredir", allure_results_dir])

        print(f"🔄 Запуск: {' '.join(command)}")
        print("=" * 60)

        # Устанавливаем правильную рабочую директорию
        os.chdir(current_dir)

        # Создаем директории для отчетов
        os.makedirs(allure_results_dir, exist_ok=True)
        os.makedirs(allure_report_dir, exist_ok=True)

        result = subprocess.run(command)

        # Предлагаем открыть отчет после завершения
        if allure_installed and result.returncode in [0, 1]:
            open_report = input("\n📊 Хотите открыть Allure отчет? (y/n): ").strip().lower()
            if open_report == 'y':
                generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)
        elif not allure_installed:
            print("\n📊 Allure не установлен. Отчет не может быть сгенерирован.")

        sys.exit(result.returncode)

    elif choice == "6":
        if not allure_installed:
            print("❌ Allure не установлен. Сначала установите Allure.")
            sys.exit(1)

        command = commands[5]  # Запуск с генерацией Allure
        print(f"🔄 Запуск: {' '.join(command)}")
        print("=" * 60)

        os.chdir(current_dir)
        os.makedirs(allure_results_dir, exist_ok=True)
        os.makedirs(allure_report_dir, exist_ok=True)

        result = subprocess.run(command)

        if result.returncode in [0, 1]:
            open_report = input("\n📊 Хотите открыть Allure отчет? (y/n): ").strip().lower()
            if open_report == 'y':
                generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)

        sys.exit(result.returncode)

    elif choice == "7":
        command = commands[6]  # Параллельный запуск

        print(f"🔄 Запуск: {' '.join(command)}")
        print("=" * 60)

        os.chdir(current_dir)
        os.makedirs(allure_results_dir, exist_ok=True)
        os.makedirs(allure_report_dir, exist_ok=True)

        result = subprocess.run(command)

        if allure_installed and result.returncode in [0, 1]:
            open_report = input("\n📊 Хотите открыть Allure отчет? (y/n): ").strip().lower()
            if open_report == 'y':
                generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)
        elif not allure_installed:
            print("\n📊 Allure не установлен. Отчет не может быть сгенерирован.")

        sys.exit(result.returncode)

    elif choice == "8":
        if not allure_installed:
            print("❌ Allure не установлен. Сначала установите Allure.")
            sys.exit(1)

        print("🎯 Генерация Allure отчета из существующих результатов")
        generate_and_open_report(allure_path, allure_results_dir, allure_report_dir)

    else:
        print("❌ Неверный выбор")
        sys.exit(1)


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