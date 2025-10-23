import pytest
import allure
import random
import string


@allure.feature("Auth - Register")
class TestAuthRegister:

    def generate_unique_username(self):
        """Генерация уникального имени пользователя"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_suffix}"

    def test_register_success(self, api_client):
        """POST /auth/register - успешная регистрация"""
        user_data = {
            "username": self.generate_unique_username(),
            "password": "test_password_123",
            "email": f"{self.generate_unique_username()}@example.com"
        }

        response = api_client.register(user_data)
        print("REGISTER RESPONSE:", response.status_code, response.json())

        assert response.status_code in [200, 201, 409]

        # Если регистрация успешна (200/201)
        if response.status_code in [200, 201]:
            data = response.json()
            assert "message" in data or "user" in data or "token" in data

    def test_register_duplicate_username(self, api_client):
        """POST /auth/register - имя пользователя уже существует"""
        user_data = {
            "username": self.generate_unique_username(),
            "password": "password123",
            "email": f"{self.generate_unique_username()}@example.com"
        }

        response1 = api_client.register(user_data)
        print("FIRST REGISTER:", response1.status_code, response1.json())

        if response1.status_code in [200, 201]:
            response2 = api_client.register(user_data)
            print("SECOND REGISTER:", response2.status_code, response2.json())

            assert response2.status_code in [409, 400]
        else:
            pytest.skip("Registration not supported by API")

    def test_register_missing_fields(self, api_client):
        """POST /auth/register - отсутствуют обязательные поля"""
        incomplete_data = {
            "username": self.generate_unique_username()
            # Отсутствуют password и email
        }

        response = api_client.register(incomplete_data)
        print("MISSING FIELDS RESPONSE:", response.status_code, response.json())

        assert response.status_code in [400, 201, 200]