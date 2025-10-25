#!/usr/bin/env python3
"""
Проверка доступности Allure
"""
import subprocess
import os
import sys


def check_allure():
    """Проверка различных способов запуска Allure"""

    print("🔍 Проверка доступности Allure...")

    # Способ 1: Простой вызов
    print("\n1. Проверка: allure --version")
    try:
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Allure доступен: {result.stdout.strip()}")
            return True
        else:
            print("❌ Allure не доступен через простой вызов")
    except FileNotFoundError:
        print("❌ Allure не найден в PATH")

    # Способ 2: Полный путь
    print("\n2. Проверка: полный путь к Allure")
    allure_paths = [
        r"C:\allure\allure-2.35.1\bin\allure.bat",
        r"C:\allure\allure-2.35.1\bin\allure",
        r"C:\allure\bin\allure.bat"
    ]

    for allure_path in allure_paths:
        if os.path.exists(allure_path):
            print(f"✅ Найден Allure: {allure_path}")
            try:
                result = subprocess.run([allure_path, "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Allure работает: {result.stdout.strip()}")
                    return allure_path
            except Exception as e:
                print(f"❌ Ошибка при запуске {allure_path}: {e}")

    # Способ 3: Поиск в PATH
    print("\n3. Поиск Allure в PATH")
    paths = os.environ.get("PATH", "").split(";")
    for path in paths:
        allure_exe = os.path.join(path, "allure.bat")
        if os.path.exists(allure_exe):
            print(f"✅ Найден в PATH: {allure_exe}")
            try:
                result = subprocess.run([allure_exe, "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Allure работает: {result.stdout.strip()}")
                    return allure_exe
            except Exception as e:
                print(f"❌ Ошибка при запуске {allure_exe}: {e}")

    print("\n❌ Allure не найден или не работает")
    return False


if __name__ == "__main__":
    check_allure()