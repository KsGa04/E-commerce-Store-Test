import pytest
import allure


@allure.feature("Reviews - GET")
class TestReviewsGet:

    def test_get_reviews_success(self, api_client):
        """GET /products/{id}/review - получить отзывы товара"""
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = api_client.get_reviews(product_id)
        assert response.status_code == 200

        data = response.json()
        assert "reviews" in data
        assert "total" in data
        assert isinstance(data["reviews"], list)

    def test_get_reviews_nonexistent_product(self, api_client):
        """GET /products/{id}/review - несуществующий товар"""
        response = api_client.get_reviews("nonexistent-id")
        assert response.status_code == 404