import pytest
import allure

@pytest.mark.api
@pytest.mark.auth
@allure.feature("Auth - Login")
@allure.severity(allure.severity_level.BLOCKER)
class TestAuthLogin:

    @allure.story("Успешная авторизация")
    @allure.description("Проверка успешного входа с валидными учетными данными")
    @allure.tag("auth", "login", "positive")
    def test_login_success(self, api_client):
        """POST /auth/login - успешная авторизация"""
        with allure.step("Выполнить запрос на авторизацию с валидными данными"):
            response = api_client.login("admin", "admin123")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "token" in data
            assert "user" in data
            assert api_client.token is not None

        allure.attach(f"Response: {response.text}", name="Response Body", attachment_type=allure.attachment_type.TEXT)

    @allure.story("Неверные учетные данные")
    @allure.description("Проверка ошибки при неверном имени пользователя")
    @allure.tag("auth", "login", "negative")
    def test_login_invalid_username(self, api_client):
        """POST /auth/login - неверное имя пользователя"""
        with allure.step("Выполнить запрос с неверным именем пользователя"):
            response = api_client.login("wrong_user", "admin123")

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401

        allure.attach(f"Response: {response.text}", name="Error Response", attachment_type=allure.attachment_type.TEXT)

    @allure.story("Неверные учетные данные")
    @allure.description("Проверка ошибки при неверном пароле")
    @allure.tag("auth", "login", "negative")
    def test_login_invalid_password(self, api_client):
        """POST /auth/login - неверный пароль"""
        with allure.step("Выполнить запрос с неверным паролем"):
            response = api_client.login("admin", "wrong_password")

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401

    @allure.story("Отсутствующие данные")
    @allure.description("Проверка ошибки при отсутствии учетных данных")
    @allure.tag("auth", "login", "negative", "validation")
    def test_login_missing_credentials(self, api_client):
        """POST /auth/login - отсутствуют учетные данные"""
        with allure.step("Выполнить запрос с пустыми учетными данными"):
            response = api_client.login("", "")

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Отсутствующие данные")
    @allure.description("Проверка ошибки при отсутствии пароля")
    @allure.tag("auth", "login", "negative", "validation")
    def test_login_missing_password(self, api_client):
        """POST /auth/login - отсутствует пароль"""
        with allure.step("Выполнить запрос без пароля"):
            response = api_client.login("admin", "")

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Отсутствующие данные")
    @allure.description("Проверка ошибки при отсутствии имени пользователя")
    @allure.tag("auth", "login", "negative", "validation")
    def test_login_missing_username(self, api_client):
        """POST /auth/login - отсутствует имя пользователя"""
        with allure.step("Выполнить запрос без имени пользователя"):
            response = api_client.login("", "admin123")

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Безопасность")
    @allure.description("Проверка защиты от SQL инъекций")
    @allure.tag("auth", "login", "security", "negative")
    def test_login_sql_injection_attempt(self, api_client):
        """POST /auth/login - попытка SQL инъекции"""
        with allure.step("Выполнить запрос с SQL инъекцией в имени пользователя"):
            response = api_client.login("admin' OR '1'='1", "password")

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401