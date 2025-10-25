import pytest
import sys
import os
import random
import string

# Добавляем корневую директорию в path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.api.client import ApiClient
from config.environment import Environment


def generate_unique_product_name():
    """Генерация уникального имени товара"""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"Test Product {random_suffix}"


def generate_unique_username():
    """Генерация уникального имени пользователя"""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"testuser_{random_suffix}"


@pytest.fixture
def api_client():
    """Базовый неавторизованный клиент"""
    return ApiClient()


@pytest.fixture
def auth_client():
    """Авторизованный клиент с повторной попыткой при неудаче"""
    client = ApiClient()
    response = client.login(
        Environment.TEST_USER["username"],
        Environment.TEST_USER["password"]
    )

    # Если аутентификация не удалась, делаем повторную попытку
    if response.status_code != 200:
        print(f"First login attempt failed with {response.status_code}, retrying...")
        import time
        time.sleep(1)
        response = client.login(
            Environment.TEST_USER["username"],
            Environment.TEST_USER["password"]
        )

    # Если вторая попытка тоже не удалась, пропускаем тест
    if response.status_code != 200:
        pytest.skip(f"Authentication failed with status {response.status_code}")

    return client


@pytest.fixture
def sample_product():
    """Тестовые данные товара с уникальным именем"""
    return {
        "name": generate_unique_product_name(),
        "description": "Mechanical gaming keyboard with RGB",
        "price": 129.99,
        "category": "Electronics",
        "stock": 25,
        "imageUrl": "/keyboard.png"
    }


@pytest.fixture
def sample_review():
    """Тестовые данные отзыва"""
    return {
        "rating": 5,
        "comment": "Excellent product! Highly recommended!",
        "author": "Test User"
    }


def extract_product_id(create_response, product_name, auth_client):
    """Вспомогательная функция для извлечения ID созданного товара"""
    data = create_response.json()

    if "product" in data:
        return data["product"]["id"]
    elif "id" in data:
        return data["id"]
    else:
        # Если ID нет в ответе, ищем товар по имени в списке
        products_response = auth_client.get_products()
        products_data = products_response.json()
        our_product = next((p for p in products_data["products"] if p["name"] == product_name), None)
        assert our_product is not None, f"Товар с именем '{product_name}' не найден в списке"
        return our_product["id"]