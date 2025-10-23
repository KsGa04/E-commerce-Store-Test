import pytest
import allure
import random
import string
from tests.api.conftest import extract_product_id


@allure.feature("Products - PUT")
class TestProductsPut:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"Test Product {random_suffix}"

    def test_put_update_product_success(self, auth_client, sample_product):
        """PUT /products/{id} - успешное полное обновление"""
        # Используем уникальное имя для создания
        unique_product = sample_product.copy()
        unique_product["name"] = self.generate_unique_product_name()

        create_response = auth_client.create_product(unique_product)
        product_id = extract_product_id(create_response, unique_product["name"], auth_client)

        update_data = {
            "name": self.generate_unique_product_name(),  # Новое уникальное имя
            "description": "Completely updated description",
            "price": 199.99,
            "category": "Home Appliances",
            "stock": 40,
            "imageUrl": "/updated-image.png"
        }

        response = auth_client.update_product(product_id, update_data, method="PUT")
        print("PUT RESPONSE:", response.json())
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "product" in data

        updated_product = data["product"]
        assert updated_product["name"] == update_data["name"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["category"] == update_data["category"]

    def test_put_update_missing_required_fields(self, auth_client, sample_product):
        """PUT /products/{id} - отсутствуют обязательные поля"""
        create_response = auth_client.create_product(sample_product)
        product_id = extract_product_id(create_response, sample_product["name"], auth_client)

        incomplete_data = {
            "name": "Incomplete Update",
            "price": 150.00
            # Отсутствуют category, stock
        }

        response = auth_client.update_product(product_id, incomplete_data, method="PUT")
        assert response.status_code == 400

        error_data = response.json()
        assert "error" in error_data
        assert "required" in error_data

    def test_put_update_nonexistent_product(self, auth_client):
        """PUT /products/{id} - несуществующий товар"""
        update_data = {
            "name": "Nonexistent Product",
            "description": "Description",
            "price": 100.00,
            "category": "Test",
            "stock": 10
        }

        response = auth_client.update_product("nonexistent-id", update_data, method="PUT")
        assert response.status_code == 404

    def test_put_update_unauthorized(self, api_client):
        """PUT /products/{id} - неавторизованный доступ"""
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        update_data = {
            "name": "Unauthorized Update",
            "description": "Description",
            "price": 100.00,
            "category": "Test",
            "stock": 10
        }

        response = api_client.update_product(product_id, update_data, method="PUT")
        assert response.status_code == 401