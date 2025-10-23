import pytest
import allure
from tests.api.conftest import extract_product_id


@allure.feature("Products - POST")
class TestProductsPost:

    def test_create_product_success(self, auth_client, sample_product):
        """POST /products - успешное создание товара"""
        response = auth_client.create_product(sample_product)
        assert response.status_code == 201

        data = response.json()
        # Проверяем различные возможные структуры ответа
        if "product" in data:
            created_product = data["product"]
        elif "message" in data:
            # Если возвращается сообщение, проверяем через список товаров
            products_response = auth_client.get_products()
            products_data = products_response.json()
            our_product = next((p for p in products_data["products"] if p["name"] == sample_product["name"]), None)
            assert our_product is not None
            created_product = our_product
        else:
            created_product = data

        assert created_product["name"] == sample_product["name"]
        assert created_product["price"] == sample_product["price"]
        assert created_product["category"] == sample_product["category"]

    def test_create_product_duplicate_name(self, auth_client, sample_product):
        """POST /products - товар с таким именем уже существует"""
        # Первое создание
        response1 = auth_client.create_product(sample_product)
        assert response1.status_code == 201

        # Второе создание с тем же именем
        response2 = auth_client.create_product(sample_product)
        assert response2.status_code == 409

    def test_create_product_missing_required_fields(self, auth_client):
        """POST /products - отсутствуют обязательные поля"""
        incomplete_data = {
            "name": "Incomplete Product"
            # Отсутствуют price, category, stock
        }

        response = auth_client.create_product(incomplete_data)
        assert response.status_code == 400

    def test_create_product_unauthorized(self, api_client, sample_product):
        """POST /products - неавторизованный доступ"""
        response = api_client.create_product(sample_product)
        assert response.status_code == 401