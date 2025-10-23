import pytest
from src.api.client import ApiClient


class TestProductsFilters:
    def test_filter_by_category(self):
        """Тест фильтрации по категории"""
        client = ApiClient()

        # Фильтруем по категории Electronics
        response = client.get_products({"category": "Electronics"})
        assert response.status_code == 200

        data = response.json()
        products = data["products"]

        # Проверяем, что все товары в категории Electronics
        for product in products:
            assert product["category"] == "Electronics"

    def test_filter_by_price_range(self):
        """Тест фильтрации по диапазону цен"""
        client = ApiClient()

        # Фильтруем по цене от 100 до 300
        response = client.get_products({
            "minPrice": 100,
            "maxPrice": 300
        })
        assert response.status_code == 200

        data = response.json()
        products = data["products"]

        # Проверяем, что цены в диапазоне
        for product in products:
            assert 100 <= product["price"] <= 300

    def test_filter_by_category_and_price(self):
        """Тест комбинированной фильтрации"""
        client = ApiClient()

        response = client.get_products({
            "category": "Electronics",
            "minPrice": 200,
            "maxPrice": 500
        })
        assert response.status_code == 200

        data = response.json()
        products = data["products"]

        for product in products:
            assert product["category"] == "Electronics"
            assert 200 <= product["price"] <= 500

    def test_search_products(self):
        """Тест поиска товаров"""
        client = ApiClient()

        # Ищем товары с "headphones" в названии
        response = client.get_products({"search": "headphones"})
        assert response.status_code == 200

        data = response.json()
        products = data["products"]

        # Проверяем, что в названии есть headphones
        for product in products:
            assert "headphone" in product["name"].lower()

    def test_get_categories(self):
        """Тест получения списка категорий"""
        client = ApiClient()

        response = client.get_categories()
        assert response.status_code == 200

        data = response.json()
        # Согласно скриншоту, ответ содержит объект с полями categories и total
        assert "categories" in data
        assert "total" in data

        categories = data["categories"]
        assert isinstance(categories, list)
        assert len(categories) > 0