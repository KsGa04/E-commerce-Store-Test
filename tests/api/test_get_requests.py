import pytest
import allure
from tests.api.conftest import extract_product_id


@allure.feature("GET Requests")
class TestGetRequests:

    def test_get_all_products(self, api_client):
        """Тест получения всех товаров"""
        response = api_client.get_products()

        assert response.status_code == 200
        data = response.json()

        assert "products" in data
        assert "total" in data
        assert isinstance(data["products"], list)
        assert len(data["products"]) > 0

        # Проверяем структуру первого товара
        first_product = data["products"][0]
        required_fields = ["id", "name", "price", "category", "stock"]
        for field in required_fields:
            assert field in first_product

    @pytest.mark.parametrize("filters", [
        {"category": "Electronics"},
        {"minPrice": 100, "maxPrice": 300},
        {"category": "Electronics", "minPrice": 200, "maxPrice": 500},
        {"search": "headphones"}
    ])
    def test_get_products_with_filters(self, api_client, filters):
        """Тест фильтрации товаров"""
        response = api_client.get_products(filters=filters)
        assert response.status_code == 200

        data = response.json()
        products = data["products"]

        # Валидация фильтров
        if "category" in filters:
            for product in products:
                assert product["category"] == filters["category"]

        if "minPrice" in filters:
            for product in products:
                assert product["price"] >= filters["minPrice"]

        if "maxPrice" in filters:
            for product in products:
                assert product["price"] <= filters["maxPrice"]

    def test_get_single_product(self, api_client):
        """Тест получения одного товара по ID"""
        # Сначала получаем список товаров
        products_response = api_client.get_products()
        first_product_id = products_response.json()["products"][0]["id"]

        # Получаем конкретный товар
        response = api_client.get_product(first_product_id)
        assert response.status_code == 200

        data = response.json()
        assert "product" in data
        product = data["product"]
        assert product["id"] == first_product_id

    def test_get_categories(self, api_client):
        """Тест получения списка категорий"""
        response = api_client.get_categories()
        assert response.status_code == 200

        data = response.json()
        assert "categories" in data
        assert "total" in data
        categories = data["categories"]

        assert isinstance(categories, list)
        assert len(categories) > 0
        # Проверяем, что есть ожидаемые категории
        assert "Electronics" in categories
        assert "Home" in categories

    def test_get_reviews(self, api_client):
        """Тест получения отзывов для товара"""
        # Получаем ID первого товара
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = api_client.get_reviews(product_id)
        assert response.status_code == 200

        data = response.json()
        assert "reviews" in data
        assert "total" in data
        reviews = data["reviews"]
        assert isinstance(reviews, list)

    def test_get_nonexistent_product(self, api_client):
        """Тест получения несуществующего товара"""
        response = api_client.get_product("nonexistent-id")
        assert response.status_code == 404

        error_data = response.json()
        assert "error" in error_data

    def test_get_reviews_nonexistent_product(self, api_client):
        """Тест получения отзывов для несуществующего товара"""
        response = api_client.get_reviews("nonexistent-id")
        assert response.status_code == 404