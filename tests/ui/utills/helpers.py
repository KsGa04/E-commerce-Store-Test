import time
import os
from typing import Any, Dict


class Helpers:
    """Вспомогательные функции для тестов"""

    @staticmethod
    def take_screenshot(page, name: str):
        """Создание скриншота"""
        timestamp = int(time.time())
        # Создаем директорию для скриншотов если не существует
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    @staticmethod
    def wait_for_network_idle(page, timeout: int = 5000):
        """Ожидание завершения сетевых запросов"""
        page.wait_for_load_state("networkidle", timeout=timeout)

    @staticmethod
    def get_test_data() -> Dict[str, Any]:
        """Получение тестовых данных"""
        return {
            "valid_credentials": {
                "username": "admin",
                "password": "admin123"
            },
            "invalid_credentials": {
                "username": "wronguser",
                "password": "wrongpass"
            },
            "base_url": "https://v0-swagger-backend-frontend.vercel.app"
        }

    @staticmethod
    def debug_page_info(page):
        """Вывод отладочной информации о странице"""
        print("=== PAGE DEBUG INFO ===")
        print(f"URL: {page.url}")
        print(f"Title: {page.title()}")
        print("=== END DEBUG INFO ===")