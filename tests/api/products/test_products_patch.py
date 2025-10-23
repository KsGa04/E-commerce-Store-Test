import pytest
import allure
from tests.api.conftest import extract_product_id


@allure.feature("Products - PATCH")
class TestProductsPatch:

    def test_patch_update_product_success(self, auth_client, sample_product):
        """PATCH /products/{id} - успешное частичное обновление"""
        create_response = auth_client.create_product(sample_product)
        product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        patch_data = {
            "price": 89.99,
            "stock": 15
        }

        response = auth_client.update_product(product_id, patch_data, method="PATCH")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "product" in data

        updated_product = data["product"]
        assert updated_product["price"] == patch_data["price"]
        assert updated_product["stock"] == patch_data["stock"]
        assert updated_product["name"] == sample_product["name"]  # Имя не изменилось

    def test_patch_single_field(self, auth_client, sample_product):
        """PATCH /products/{id} - обновление одного поля"""
        create_response = auth_client.create_product(sample_product)
        product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        patch_data = {"price": 79.99}

        response = auth_client.update_product(product_id, patch_data, method="PATCH")
        assert response.status_code == 200

        data = response.json()
        updated_product = data["product"]
        assert updated_product["price"] == patch_data["price"]
        assert updated_product["name"] == sample_product["name"]

    def test_patch_nonexistent_product(self, auth_client):
        """PATCH /products/{id} - несуществующий товар"""
        patch_data = {"price": 99.99}

        response = auth_client.update_product("nonexistent-id", patch_data, method="PATCH")
        assert response.status_code == 404

    def test_patch_unauthorized(self, api_client):
        """PATCH /products/{id} - неавторизованный доступ"""
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        patch_data = {"price": 99.99}

        response = api_client.update_product(product_id, patch_data, method="PATCH")
        assert response.status_code == 401