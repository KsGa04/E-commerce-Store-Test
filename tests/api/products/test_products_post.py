import pytest
import allure
import random
import string
from tests.api.conftest import extract_product_id

@pytest.mark.api
@pytest.mark.products
@allure.feature("Products - POST")
@allure.severity(allure.severity_level.CRITICAL)
class TestProductsPost:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"Test Product {random_suffix}"

    @allure.story("Создание товара")
    @allure.description("Проверка успешного создания товара")
    @allure.tag("products", "post", "positive")
    def test_create_product_success(self, auth_client, sample_product):
        """POST /products - успешное создание товара"""
        with allure.step("Сгенерировать уникальное имя товара"):
            unique_product = sample_product.copy()
            unique_product["name"] = self.generate_unique_product_name()
            allure.attach(str(unique_product), name="Product Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос на создание товара"):
            response = auth_client.create_product(unique_product)
            allure.attach(f"Create Response: {response.status_code}\n{response.text}",
                          name="Create Product Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 201"):
            assert response.status_code == 201

        with allure.step("Проверить структуру ответа и данные товара"):
            data = response.json()
            if "product" in data:
                created_product = data["product"]
            elif "message" in data:
                products_response = auth_client.get_products()
                products_data = products_response.json()
                our_product = next((p for p in products_data["products"] if p["name"] == unique_product["name"]), None)
                assert our_product is not None
                created_product = our_product
            else:
                created_product = data

            assert created_product["name"] == unique_product["name"]
            assert created_product["price"] == unique_product["price"]
            assert created_product["category"] == unique_product["category"]

    @allure.story("Дублирование товара")
    @allure.description("Проверка ошибки при создании товара с существующим именем")
    @allure.tag("products", "post", "negative")
    def test_create_product_duplicate_name(self, auth_client, sample_product):
        """POST /products - товар с таким именем уже существует"""
        with allure.step("Сгенерировать уникальное имя для первого товара"):
            unique_product = sample_product.copy()
            unique_product["name"] = self.generate_unique_product_name()

        with allure.step("Создать первый товар"):
            response1 = auth_client.create_product(unique_product)
            allure.attach(f"First Create: {response1.status_code}",
                          name="First Create Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert response1.status_code == 201

        with allure.step("Попытаться создать второй товар с тем же именем"):
            response2 = auth_client.create_product(unique_product)
            allure.attach(f"Second Create: {response2.status_code}",
                          name="Second Create Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить конфликт 409"):
            assert response2.status_code == 409

        with allure.step("Проверить структуру ошибки"):
            error_data = response2.json()
            assert "error" in error_data

    @allure.story("Валидация данных")
    @allure.description("Проверка ошибки при отсутствии обязательных полей")
    @allure.tag("products", "post", "negative", "validation")
    def test_create_product_missing_required_fields(self, auth_client):
        """POST /products - отсутствуют обязательные поля"""
        with allure.step("Создать данные без обязательных полей"):
            incomplete_data = {
                "name": self.generate_unique_product_name()
            }
            allure.attach(str(incomplete_data), name="Incomplete Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос с неполными данными"):
            response = auth_client.create_product(incomplete_data)
            allure.attach(f"Missing Fields Response: {response.status_code}",
                          name="Missing Fields Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

        with allure.step("Проверить структуру ошибки"):
            error_data = response.json()
            assert "error" in error_data

    @allure.story("Проверка авторизации")
    @allure.description("Проверка ошибки при неавторизованном создании")
    @allure.tag("products", "post", "auth", "negative")
    def test_create_product_unauthorized(self, api_client, sample_product):
        """POST /products - неавторизованный доступ"""
        with allure.step("Сгенерировать уникальное имя товара"):
            unique_product = sample_product.copy()
            unique_product["name"] = self.generate_unique_product_name()

        with allure.step("Попытаться создать товар без авторизации"):
            response = api_client.create_product(unique_product)
            allure.attach(f"Unauthorized Create: {response.status_code}",
                          name="Unauthorized Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401