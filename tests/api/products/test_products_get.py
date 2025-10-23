import pytest
import allure


@allure.feature("Products - GET")
class TestProductsGet:

    def test_get_all_products(self, api_client):
        """GET /products - получить все товары"""
        response = api_client.get_products()

        assert response.status_code == 200
        data = response.json()

        assert "products" in data
        assert "total" in data
        assert isinstance(data["products"], list)
        assert len(data["products"]) > 0

    def test_get_products_filter_by_category(self, api_client):
        """GET /products?category=Electronics - фильтрация по категории"""
        response = api_client.get_products({"category": "Electronics"})
        assert response.status_code == 200

        data = response.json()
        for product in data["products"]:
            assert product["category"] == "Electronics"

    def test_get_products_filter_by_price(self, api_client):
        """GET /products?minPrice=100&maxPrice=300 - фильтрация по цене"""
        response = api_client.get_products({
            "minPrice": 100,
            "maxPrice": 300
        })
        assert response.status_code == 200

        data = response.json()
        for product in data["products"]:
            assert 100 <= product["price"] <= 300

    def test_get_products_search(self, api_client):
        """GET /products?search=headphones - поиск товаров"""
        response = api_client.get_products({"search": "headphones"})
        assert response.status_code == 200

        data = response.json()
        for product in data["products"]:
            assert "headphone" in product["name"].lower()

    def test_get_products_invalid_filters(self, api_client):
        """GET /products - невалидные параметры фильтрации"""
        # Отрицательные цены - API может их игнорировать или обрабатывать
        response = api_client.get_products({"minPrice": -10})
        print("NEGATIVE PRICE RESPONSE:", response.status_code, response.json())

        # API может вернуть 200 с пустым списком или проигнорировать фильтр
        assert response.status_code == 200

        # minPrice > maxPrice - API может игнорировать или менять местами
        response = api_client.get_products({"minPrice": 500, "maxPrice": 100})
        print("INVERTED PRICE RANGE:", response.status_code, response.json())
        assert response.status_code == 200

        # Несуществующая категория
        response = api_client.get_products({"category": "NonexistentCategory"})
        print("NONEXISTENT CATEGORY:", response.status_code, response.json())
        assert response.status_code == 200
        # Должен вернуть пустой список
        assert len(response.json()["products"]) == 0

        # Слишком длинный search запрос
        long_search = "a" * 1000
        response = api_client.get_products({"search": long_search})
        print("LONG SEARCH:", response.status_code, response.json())
        assert response.status_code == 200

    def test_get_single_product(self, api_client):
        """GET /products/{id} - получить товар по ID"""
        # Сначала получаем список товаров
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = api_client.get_product(product_id)
        assert response.status_code == 200

        data = response.json()
        assert "product" in data
        assert data["product"]["id"] == product_id

    def test_get_nonexistent_product(self, api_client):
        """GET /products/{id} - несуществующий товар"""
        response = api_client.get_product("nonexistent-id")
        assert response.status_code == 404
