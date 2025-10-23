import pytest
import allure


@allure.feature("Auth - Register")
class TestAuthRegister:

    def test_register_success(self, api_client):
        """POST /auth/register - успешная регистрация"""
        user_data = {
            "username": "test_user_123",
            "password": "test_password_123",
            "email": "test@example.com"
        }

        response = api_client.register(user_data)
        # Может вернуть 200 или 201 в зависимости от реализации
        assert response.status_code in [200, 201]

    def test_register_duplicate_username(self, api_client):
        """POST /auth/register - имя пользователя уже существует"""
        user_data = {
            "username": "admin",  # Уже существует
            "password": "password123",
            "email": "admin@example.com"
        }

        response = api_client.register(user_data)
        assert response.status_code == 409

    def test_register_missing_fields(self, api_client):
        """POST /auth/register - отсутствуют обязательные поля"""
        incomplete_data = {
            "username": "test_user"
            # Отсутствуют password и email
        }

        response = api_client.register(incomplete_data)
        assert response.status_code == 400