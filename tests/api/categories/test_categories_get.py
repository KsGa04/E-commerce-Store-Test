import pytest
import allure


@allure.feature("Categories - GET")
class TestCategoriesGet:

    def test_get_categories_success(self, api_client):
        """GET /categories - получить список категорий"""
        response = api_client.get_categories()
        assert response.status_code == 200

        data = response.json()
        assert "categories" in data
        assert "total" in data

        categories = data["categories"]
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert "Electronics" in categories
        assert "Home" in categories