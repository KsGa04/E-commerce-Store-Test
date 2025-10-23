import pytest
import allure
import random
import string
from tests.api.conftest import extract_product_id


@allure.feature("Products - POST")
class TestProductsPost:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"Test Product {random_suffix}"

    def test_create_product_success(self, auth_client, sample_product):
        """POST /products - успешное создание товара"""
        # Используем уникальное имя
        unique_product = sample_product.copy()
        unique_product["name"] = self.generate_unique_product_name()

        response = auth_client.create_product(unique_product)
        assert response.status_code == 201

        data = response.json()
        print("CREATE RESPONSE:", data)

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

    def test_create_product_duplicate_name(self, auth_client, sample_product):
        """POST /products - товар с таким именем уже существует"""
        # Используем уникальное имя для первого создания
        unique_product = sample_product.copy()
        unique_product["name"] = self.generate_unique_product_name()

        # Первое создание
        response1 = auth_client.create_product(unique_product)
        assert response1.status_code == 201

        # Второе создание с тем же именем
        response2 = auth_client.create_product(unique_product)
        assert response2.status_code == 409

        error_data = response2.json()
        assert "error" in error_data

    def test_create_product_missing_required_fields(self, auth_client):
        """POST /products - отсутствуют обязательные поля"""
        incomplete_data = {
            "name": self.generate_unique_product_name()
            # Отсутствуют price, category, stock
        }

        response = auth_client.create_product(incomplete_data)
        assert response.status_code == 400

        error_data = response.json()
        assert "error" in error_data

    def test_create_product_unauthorized(self, api_client, sample_product):
        """POST /products - неавторизованный доступ"""
        unique_product = sample_product.copy()
        unique_product["name"] = self.generate_unique_product_name()

        response = api_client.create_product(unique_product)
        assert response.status_code == 401