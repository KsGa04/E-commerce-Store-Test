#!/usr/bin/env python3
"""
Скрипт для проверки корректности импортов
"""
import sys
import os


def check_imports():
    """Проверка всех импортов"""

    # Добавляем корень проекта в Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)

    print("Проверка импортов...")

    try:
        from tests.ui.pages.base_page import BasePage
        print("✓ BasePage импортирован успешно")

        from tests.ui.pages.home_page import HomePage
        print("✓ HomePage импортирован успешно")

        from tests.ui.pages.login_page import LoginPage
        print("✓ LoginPage импортирован успешно")

        from tests.ui.pages.admin_page import AdminPage
        print("✓ AdminPage импортирован успешно")

        from tests.ui.utills.helpers import Helpers
        print("✓ Helpers импортирован успешно")

        print("\nВсе импорты работают корректно!")
        return True

    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False


if __name__ == "__main__":
    check_imports()