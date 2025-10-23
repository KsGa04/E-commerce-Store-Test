import pytest
import allure


@allure.feature("Reviews - POST")
class TestReviewsPost:

    def test_create_review_success(self, auth_client, sample_review):
        """POST /products/{id}/review - успешное создание отзыва"""
        api_client = auth_client
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = auth_client.create_review(product_id, sample_review)
        assert response.status_code == 201

        response_data = response.json()
        assert "message" in response_data or "review" in response_data

    def test_create_review_invalid_rating(self, auth_client):
        """POST /products/{id}/review - невалидный рейтинг"""
        api_client = auth_client
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        invalid_review = {
            "rating": 6,  # Должен быть 1-5
            "comment": "Test comment",
            "author": "Test User"
        }

        response = auth_client.create_review(product_id, invalid_review)
        assert response.status_code == 400

    def test_create_review_invalid_rating_low(self, auth_client):
        """POST /products/{id}/review - рейтинг меньше 1"""
        products_response = auth_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        invalid_review = {
            "rating": 0,  # Должен быть 1-5
            "comment": "Test comment",
            "author": "Test User"
        }
        response = auth_client.create_review(product_id, invalid_review)
        assert response.status_code == 400

    def test_create_review_missing_comment(self, auth_client):
        """POST /products/{id}/review - отсутствует комментарий"""
        products_response = auth_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        invalid_review = {
            "rating": 5,
            # Отсутствует comment
            "author": "Test User"
        }
        response = auth_client.create_review(product_id, invalid_review)
        assert response.status_code == 400

    def test_create_review_empty_comment(self, auth_client):
        """POST /products/{id}/review - пустой комментарий"""
        products_response = auth_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        invalid_review = {
            "rating": 5,
            "comment": "",  # Пустой комментарий
            "author": "Test User"
        }
        response = auth_client.create_review(product_id, invalid_review)
        assert response.status_code == 400

    def test_create_review_nonexistent_product(self, auth_client, sample_review):
        """POST /products/{id}/review - несуществующий товар"""
        response = auth_client.create_review("nonexistent-id", sample_review)
        assert response.status_code == 404

    def test_create_review_unauthorized(self, api_client, sample_review):
        """POST /products/{id}/review - неавторизованный доступ"""
        products_response = api_client.get_products()
        product_id = products_response.json()["products"][0]["id"]

        response = api_client.create_review(product_id, sample_review)
        assert response.status_code == 401