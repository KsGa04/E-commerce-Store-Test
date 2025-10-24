import pytest
import allure
from tests.api.conftest import extract_product_id

@pytest.mark.api
@pytest.mark.products
@allure.feature("Products - PATCH")
@allure.severity(allure.severity_level.NORMAL)
class TestProductsPatch:

    @allure.story("Частичное обновление")
    @allure.description("Проверка успешного частичного обновления товара")
    @allure.tag("products", "patch", "positive")
    def test_patch_update_product_success(self, auth_client, sample_product):
        """PATCH /products/{id} - успешное частичное обновление"""
        with allure.step("Создать тестовый товар"):
            create_response = auth_client.create_product(sample_product)
            product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        with allure.step("Подготовить данные для частичного обновления"):
            patch_data = {
                "price": 89.99,
                "stock": 15
            }
            allure.attach(str(patch_data), name="PATCH Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить PATCH запрос"):
            response = auth_client.update_product(product_id, patch_data, method="PATCH")
            allure.attach(f"PATCH Response: {response.status_code}",
                          name="PATCH Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "message" in data
            assert "product" in data

        with allure.step("Проверить обновленные поля"):
            updated_product = data["product"]
            assert updated_product["price"] == patch_data["price"]
            assert updated_product["stock"] == patch_data["stock"]
            assert updated_product["name"] == sample_product["name"]

    @allure.story("Обновление одного поля")
    @allure.description("Проверка обновления только одного поля товара")
    @allure.tag("products", "patch", "positive")
    def test_patch_single_field(self, auth_client, sample_product):
        """PATCH /products/{id} - обновление одного поля"""
        with allure.step("Создать тестовый товар"):
            create_response = auth_client.create_product(sample_product)
            product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        with allure.step("Подготовить данные для обновления цены"):
            patch_data = {"price": 79.99}

        with allure.step("Выполнить PATCH запрос для обновления цены"):
            response = auth_client.update_product(product_id, patch_data, method="PATCH")
            allure.attach(f"Single Field PATCH Response: {response.status_code}",
                          name="Single Field Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить обновленную цену"):
            data = response.json()
            updated_product = data["product"]
            assert updated_product["price"] == patch_data["price"]
            assert updated_product["name"] == sample_product["name"]

    @allure.story("Обновление несуществующего товара")
    @allure.description("Проверка ошибки при обновлении несуществующего товара")
    @allure.tag("products", "patch", "negative")
    def test_patch_nonexistent_product(self, auth_client):
        """PATCH /products/{id} - несуществующий товар"""
        with allure.step("Подготовить данные для обновления"):
            patch_data = {"price": 99.99}

        with allure.step("Попытаться обновить несуществующий товар"):
            response = auth_client.update_product("nonexistent-id", patch_data, method="PATCH")
            allure.attach(f"Nonexistent PATCH Response: {response.status_code}",
                          name="Nonexistent Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404

    @allure.story("Проверка авторизации")
    @allure.description("Проверка ошибки при неавторизованном обновлении")
    @allure.tag("products", "patch", "auth", "negative")
    def test_patch_unauthorized(self, api_client):
        """PATCH /products/{id} - неавторизованный доступ"""
        with allure.step("Получить ID существующего товара"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить данные для обновления"):
            patch_data = {"price": 99.99}

        with allure.step("Попытаться обновить товар без авторизации"):
            response = api_client.update_product(product_id, patch_data, method="PATCH")
            allure.attach(f"Unauthorized PATCH Response: {response.status_code}",
                          name="Unauthorized Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401