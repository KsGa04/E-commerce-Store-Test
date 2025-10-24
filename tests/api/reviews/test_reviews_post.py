import pytest
import allure

@pytest.mark.api
@pytest.mark.reviews
@allure.feature("Reviews - POST")
@allure.severity(allure.severity_level.NORMAL)
class TestReviewsPost:

    @allure.story("Создание отзыва")
    @allure.description("Проверка успешного создания отзыва")
    @allure.tag("reviews", "post", "positive")
    def test_create_review_success(self, auth_client, sample_review):
        """POST /products/{id}/review - успешное создание отзыва"""
        with allure.step("Получить ID существующего товара"):
            products_response = auth_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Выполнить запрос на создание отзыва"):
            response = auth_client.create_review(product_id, sample_review)
            allure.attach(f"Create Review Response: {response.status_code}\n{response.text}",
                          name="Create Review Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 201"):
            assert response.status_code == 201

        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert "message" in response_data or "review" in response_data

    @allure.story("Валидация рейтинга")
    @allure.description("Проверка ошибки при невалидном рейтинге (больше 5)")
    @allure.tag("reviews", "post", "negative", "validation")
    def test_create_review_invalid_rating(self, auth_client):
        """POST /products/{id}/review - невалидный рейтинг"""
        with allure.step("Получить ID существующего товара"):
            products_response = auth_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить отзыв с рейтингом 6"):
            invalid_review = {
                "rating": 6,
                "comment": "Test comment",
                "author": "Test User"
            }
            allure.attach(str(invalid_review), name="Invalid Rating Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос с невалидным рейтингом"):
            response = auth_client.create_review(product_id, invalid_review)
            allure.attach(f"Invalid Rating Response: {response.status_code}",
                          name="Invalid Rating Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Валидация рейтинга")
    @allure.description("Проверка ошибки при невалидном рейтинге (меньше 1)")
    @allure.tag("reviews", "post", "negative", "validation")
    def test_create_review_invalid_rating_low(self, auth_client):
        """POST /products/{id}/review - рейтинг меньше 1"""
        with allure.step("Получить ID существующего товара"):
            products_response = auth_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить отзыв с рейтингом 0"):
            invalid_review = {
                "rating": 0,
                "comment": "Test comment",
                "author": "Test User"
            }

        with allure.step("Выполнить запрос с рейтингом 0"):
            response = auth_client.create_review(product_id, invalid_review)
            allure.attach(f"Low Rating Response: {response.status_code}",
                          name="Low Rating Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Валидация данных")
    @allure.description("Проверка ошибки при отсутствии комментария")
    @allure.tag("reviews", "post", "negative", "validation")
    def test_create_review_missing_comment(self, auth_client):
        """POST /products/{id}/review - отсутствует комментарий"""
        with allure.step("Получить ID существующего товара"):
            products_response = auth_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить отзыв без комментария"):
            invalid_review = {
                "rating": 5,
                "author": "Test User"
            }
            allure.attach(str(invalid_review), name="Missing Comment Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос без комментария"):
            response = auth_client.create_review(product_id, invalid_review)
            allure.attach(f"Missing Comment Response: {response.status_code}",
                          name="Missing Comment Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Валидация данных")
    @allure.description("Проверка ошибки при пустом комментарии")
    @allure.tag("reviews", "post", "negative", "validation")
    def test_create_review_empty_comment(self, auth_client):
        """POST /products/{id}/review - пустой комментарий"""
        with allure.step("Получить ID существующего товара"):
            products_response = auth_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Подготовить отзыв с пустым комментарием"):
            invalid_review = {
                "rating": 5,
                "comment": "",
                "author": "Test User"
            }

        with allure.step("Выполнить запрос с пустым комментарием"):
            response = auth_client.create_review(product_id, invalid_review)
            allure.attach(f"Empty Comment Response: {response.status_code}",
                          name="Empty Comment Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400

    @allure.story("Создание отзыва несуществующему товару")
    @allure.description("Проверка ошибки при создании отзыва несуществующему товару")
    @allure.tag("reviews", "post", "negative")
    def test_create_review_nonexistent_product(self, auth_client, sample_review):
        """POST /products/{id}/review - несуществующий товар"""
        with allure.step("Попытаться создать отзыв несуществующему товару"):
            response = auth_client.create_review("nonexistent-id", sample_review)
            allure.attach(f"Nonexistent Product Review Response: {response.status_code}",
                          name="Nonexistent Product Review Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404

    @allure.story("Проверка авторизации")
    @allure.description("Проверка ошибки при неавторизованном создании отзыва")
    @allure.tag("reviews", "post", "auth", "negative")
    def test_create_review_unauthorized(self, api_client, sample_review):
        """POST /products/{id}/review - неавторизованный доступ"""
        with allure.step("Получить ID существующего товара"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step("Попытаться создать отзыв без авторизации"):
            response = api_client.create_review(product_id, sample_review)
            allure.attach(f"Unauthorized Review Response: {response.status_code}",
                          name="Unauthorized Review Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401