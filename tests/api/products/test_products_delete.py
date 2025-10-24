import pytest
import allure
from tests.api.conftest import extract_product_id

@pytest.mark.api
@pytest.mark.products
@allure.feature("Products - DELETE")
@allure.severity(allure.severity_level.CRITICAL)
class TestProductsDelete:

    @allure.story("Удаление товара")
    @allure.description("Проверка успешного удаления товара")
    @allure.tag("products", "delete", "positive")
    def test_delete_product_success(self, auth_client, sample_product):
        """DELETE /products/{id} - успешное удаление"""
        with allure.step("Создать тестовый товар"):
            create_response = auth_client.create_product(sample_product)
            product_id = extract_product_id(create_response, sample_product["name"], auth_client)
            allure.attach(f"Created Product ID: {product_id}", name="Product ID",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Удалить товар"):
            delete_response = auth_client.delete_product(product_id)
            allure.attach(f"Delete Response: {delete_response.status_code}",
                          name="Delete Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert delete_response.status_code == 200

        with allure.step("Проверить структуру ответа удаления"):
            data = delete_response.json()
            assert "message" in data
            assert "product" in data

        with allure.step("Проверить что товар больше не доступен"):
            get_response = auth_client.get_product(product_id)
            allure.attach(f"Get After Delete: {get_response.status_code}",
                          name="Post-Delete Check",
                          attachment_type=allure.attachment_type.TEXT)
            assert get_response.status_code == 404

    @allure.story("Удаление несуществующего товара")
    @allure.description("Проверка ошибки при удалении несуществующего товара")
    @allure.tag("products", "delete", "negative")
    def test_delete_nonexistent_product(self, auth_client):
        """DELETE /products/{id} - несуществующий товар"""
        with allure.step("Попытаться удалить несуществующий товар"):
            response = auth_client.delete_product("nonexistent-id")
            allure.attach(f"Response: {response.status_code}",
                          name="Delete Nonexistent Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404

    @allure.story("Проверка авторизации")
    @allure.description("Проверка ошибки при неавторизованном удалении")
    @allure.tag("products", "delete", "auth", "negative")
    def test_delete_unauthorized(self, api_client):
        """DELETE /products/{id} - неавторизованный доступ"""
        with allure.step("Получить ID существующего товара"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Попытаться удалить товар без авторизации"):
            response = api_client.delete_product(product_id)
            allure.attach(f"Unauthorized Delete Response: {response.status_code}",
                          name="Unauthorized Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401