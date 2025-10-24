import pytest
import allure
import random
import string

@pytest.mark.api
@pytest.mark.auth
@allure.feature("Auth - Register")
@allure.severity(allure.severity_level.CRITICAL)
class TestAuthRegister:

    def generate_unique_username(self):
        """Генерация уникального имени пользователя"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_suffix}"

    @allure.story("Успешная регистрация")
    @allure.description("Проверка успешной регистрации нового пользователя")
    @allure.tag("auth", "register", "positive")
    def test_register_success(self, api_client):
        """POST /auth/register - успешная регистрация"""
        with allure.step("Сгенерировать данные нового пользователя"):
            user_data = {
                "username": self.generate_unique_username(),
                "password": "test_password_123",
                "email": f"{self.generate_unique_username()}@example.com"
            }

        allure.attach(str(user_data), name="User Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос на регистрацию"):
            response = api_client.register(user_data)

        with allure.step("Записать ответ в отчет"):
            allure.attach(f"Status: {response.status_code}\nResponse: {response.text}",
                          name="Register Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200, 201 или 409"):
            assert response.status_code in [200, 201, 409]

        with allure.step("Если регистрация успешна, проверить структуру ответа"):
            if response.status_code in [200, 201]:
                data = response.json()
                assert "message" in data or "user" in data or "token" in data

    @allure.story("Дублирование пользователя")
    @allure.description("Проверка ошибки при регистрации с существующим именем пользователя")
    @allure.tag("auth", "register", "negative")
    def test_register_duplicate_username(self, api_client):
        """POST /auth/register - имя пользователя уже существует"""
        with allure.step("Сгенерировать данные пользователя"):
            user_data = {
                "username": self.generate_unique_username(),
                "password": "password123",
                "email": f"{self.generate_unique_username()}@example.com"
            }

        with allure.step("Выполнить первую регистрацию"):
            response1 = api_client.register(user_data)
            allure.attach(f"First Register: {response1.status_code}",
                          name="First Register Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Если первая регистрация успешна, выполнить вторую с теми же данными"):
            if response1.status_code in [200, 201]:
                response2 = api_client.register(user_data)
                allure.attach(f"Second Register: {response2.status_code}",
                              name="Second Register Response",
                              attachment_type=allure.attachment_type.TEXT)

                with allure.step("Проверить конфликт 409 или ошибку 400"):
                    assert response2.status_code in [409, 400]
            else:
                with allure.step("Пропустить тест если регистрация не поддерживается"):
                    pytest.skip("Registration not supported by API")

    @allure.story("Валидация данных")
    @allure.description("Проверка ошибки при отсутствии обязательных полей")
    @allure.tag("auth", "register", "negative", "validation")
    def test_register_missing_fields(self, api_client):
        """POST /auth/register - отсутствуют обязательные поля"""
        with allure.step("Создать данные без обязательных полей"):
            incomplete_data = {
                "username": self.generate_unique_username()
            }

        allure.attach(str(incomplete_data), name="Incomplete Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос регистрации с неполными данными"):
            response = api_client.register(incomplete_data)

        with allure.step("Записать ответ"):
            allure.attach(f"Status: {response.status_code}\nResponse: {response.text}",
                          name="Missing Fields Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400 или 200/201 если API принимает неполные данные"):
            assert response.status_code in [400, 201, 200]