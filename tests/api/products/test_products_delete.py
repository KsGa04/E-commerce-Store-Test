import pytest
import allure
from tests.api.conftest import extract_product_id


@allure.feature("Products - DELETE")
class TestProductsDelete:

    def test_delete_product_success(self, auth_client, sample_product):
        """DELETE /products/{id} - успешное удаление"""
        create_response = auth_client.create_product(sample_product)
        product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        delete_response = auth_client.delete_product(product_id)
        assert delete_response.status_code == 200

        data = delete_response.json()
        assert "message" in data
        assert "product" in data

        # Проверяем, что товар удален
        get_response = auth_client.get_product(product_id)
        assert get_response.status_code == 404

    def test_delete_nonexistent_product(self, auth_client):
        """DELETE /products/{id} - несуществующий товар"""
        response = auth_client.delete_product("nonexistent-id")
        assert response.status_code == 404

    def test_delete_unauthorized(self, api_client):
        """DELETE /products/{id} - неавторизованный доступ"""
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = api_client.delete_product(product_id)
        assert response.status_code == 401