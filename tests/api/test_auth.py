import pytest
from src.api.client import ApiClient
from config.environment import Environment


class TestAuthentication:
    def test_successful_login(self):
        client = ApiClient()
        response = client.login(
            Environment.TEST_USER["username"],
            Environment.TEST_USER["password"]
        )

        assert response.status_code == 200
        assert "token" in response.json()
        assert client.token is not None

    def test_get_products_public(self):
        client = ApiClient()
        response = client.get_products()

        assert response.status_code == 200
        data = response.json()
        # Проверяем, что ответ является словарем
        assert isinstance(data, dict)
        # Проверяем наличие ключа 'products'
        assert 'products' in data
        # Проверяем, что 'products' - это список
        assert isinstance(data['products'], list)
        # Проверяем наличие ключа 'total'
        assert 'total' in data

    def test_get_single_product(self):
        """Тест получения одного товара по ID"""
        client = ApiClient()

        # Сначала получаем список товаров
        products_response = client.get_products()
        assert products_response.status_code == 200

        products_data = products_response.json()
        if products_data["products"]:
            first_product_id = products_data["products"][0]["id"]

            # Получаем конкретный товар по ID
            product_response = client.get_product(first_product_id)
            assert product_response.status_code == 200

            product_data = product_response.json()
            # Согласно скриншоту, ответ содержит объект product
            assert "product" in product_data
            product = product_data["product"]
            assert "id" in product
            assert product["id"] == first_product_id
