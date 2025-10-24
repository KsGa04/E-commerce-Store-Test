import pytest
import allure
import random
import string
from tests.api.conftest import extract_product_id

@pytest.mark.api
@pytest.mark.products
@allure.feature("Products - PUT")
@allure.severity(allure.severity_level.NORMAL)
class TestProductsPut:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"Test Product {random_suffix}"

    @allure.story("Полное обновление")
    @allure.description("Проверка успешного полного обновления товара")
    @allure.tag("products", "put", "positive")
    def test_put_update_product_success(self, auth_client, sample_product):
        """PUT /products/{id} - успешное полное обновление"""
        with allure.step("Создать товар для обновления"):
            unique_product = sample_product.copy()
            unique_product["name"] = self.generate_unique_product_name()
            create_response = auth_client.create_product(unique_product)
            product_id = extract_product_id(create_response, unique_product["name"], auth_client)

        with allure.step("Подготовить данные для полного обновления"):
            update_data = {
                "name": self.generate_unique_product_name(),
                "description": "Completely updated description",
                "price": 199.99,
                "category": "Home Appliances",
                "stock": 40,
                "imageUrl": "/updated-image.png"
            }
            allure.attach(str(update_data), name="PUT Update Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить PUT запрос"):
            response = auth_client.update_product(product_id, update_data, method="PUT")
            allure.attach(f"PUT Response: {response.status_code}\n{response.text}",
                          name="PUT Update Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "message" in data
            assert "product" in data

        with allure.step("Проверить обновленные данные"):
            updated_product = data["product"]
            assert updated_product["name"] == update_data["name"]
            assert updated_product["price"] == update_data["price"]
            assert updated_product["category"] == update_data["category"]

    @allure.story("Валидация данных")
    @allure.description("Проверка ошибки при отсутствии обязательных полей при обновлении")
    @allure.tag("products", "put", "negative", "validation")
    def test_put_update_missing_required_fields(self, auth_client, sample_product):
        """PUT /products/{id} - отсутствуют обязательные поля"""
        with allure.step("Создать товар для обновления"):
            create_response = auth_client.create_product(sample_product)
            product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        with allure.step("Подготовить неполные данные для обновления"):
            incomplete_data = {
                "name": "Incomplete Update",
                "price": 150.00
            }
            allure.attach(str(incomplete_data), name="Incomplete Update Data",
                          attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить PUT запрос с неполными данными"):
            response = auth_client.update_product(product_id, incomplete_data, method="PUT")
            allure.attach(f"Incomplete PUT Response: {response.status_code}",
                          name="Incomplete PUT Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

        with allure.step("Проверить структуру ошибки"):
            error_data = response.json()
            assert "error" in error_data
            assert "required" in error_data

    @allure.story("Обновление несуществующего товара")
    @allure.description("Проверка ошибки при обновлении несуществующего товара")
    @allure.tag("products", "put", "negative")
    def test_put_update_nonexistent_product(self, auth_client):
        """PUT /products/{id} - несуществующий товар"""
        with allure.step("Подготовить данные для обновления"):
            update_data = {
                "name": "Nonexistent Product",
                "description": "Description",
                "price": 100.00,
                "category": "Test",
                "stock": 10
            }

        with allure.step("Попытаться обновить несуществующий товар"):
            response = auth_client.update_product("nonexistent-id", update_data, method="PUT")
            allure.attach(f"Nonexistent PUT Response: {response.status_code}",
                          name="Nonexistent PUT Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404

    @allure.story("Проверка авторизации")
    @allure.description("Проверка ошибки при неавторизованном обновлении")
    @allure.tag("products", "put", "auth", "negative")
    def test_put_update_unauthorized(self, api_client):
        """PUT /products/{id} - неавторизованный доступ"""
        with allure.step("Получить ID существующего товара"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить данные для обновления"):
            update_data = {
                "name": "Unauthorized Update",
                "description": "Description",
                "price": 100.00,
                "category": "Test",
                "stock": 10
            }

        with allure.step("Попытаться обновить товар без авторизации"):
            response = api_client.update_product(product_id, update_data, method="PUT")
            allure.attach(f"Unauthorized PUT Response: {response.status_code}",
                          name="Unauthorized PUT Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401