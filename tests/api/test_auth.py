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