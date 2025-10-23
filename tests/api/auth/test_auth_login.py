import pytest
import allure


@allure.feature("Auth - Login")
class TestAuthLogin:

    def test_login_success(self, api_client):
        """POST /auth/login - успешная авторизация"""
        response = api_client.login("admin", "admin123")

        assert response.status_code == 200
        data = response.json()

        assert "token" in data
        assert "user" in data
        assert api_client.token is not None

    def test_login_invalid_username(self, api_client):
        """POST /auth/login - неверное имя пользователя"""
        response = api_client.login("wrong_user", "admin123")
        assert response.status_code == 401

    def test_login_invalid_password(self, api_client):
        """POST /auth/login - неверный пароль"""
        response = api_client.login("admin", "wrong_password")
        assert response.status_code == 401

    def test_login_missing_credentials(self, api_client):
        """POST /auth/login - отсутствуют учетные данные"""
        response = api_client.login("", "")
        assert response.status_code == 400