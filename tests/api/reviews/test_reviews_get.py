import pytest
import allure

@pytest.mark.api
@pytest.mark.reviews
@allure.feature("Reviews - GET")
@allure.severity(allure.severity_level.NORMAL)
class TestReviewsGet:

    @allure.story("Получение отзывов")
    @allure.description("Проверка успешного получения отзывов товара")
    @allure.tag("reviews", "get", "positive")
    def test_get_reviews_success(self, api_client):
        """GET /products/{id}/review - получить отзывы товара"""
        with allure.step("Получить ID существующего товара"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]
            allure.attach(f"Product ID: {product_id}", name="Product ID", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Выполнить запрос на получение отзывов"):
            response = api_client.get_reviews(product_id)
            allure.attach(f"Get Reviews Response: {response.status_code}",
                          name="Get Reviews Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "reviews" in data
            assert "total" in data
            assert isinstance(data["reviews"], list)

        allure.attach(f"Total reviews: {data['total']}", name="Reviews Count",
                      attachment_type=allure.attachment_type.TEXT)

    @allure.story("Получение отзывов несуществующего товара")
    @allure.description("Проверка ошибки при получении отзывов несуществующего товара")
    @allure.tag("reviews", "get", "negative")
    def test_get_reviews_nonexistent_product(self, api_client):
        """GET /products/{id}/review - несуществующий товар"""
        with allure.step("Попытаться получить отзывы несуществующего товара"):
            response = api_client.get_reviews("nonexistent-id")
            allure.attach(f"Nonexistent Reviews Response: {response.status_code}",
                          name="Nonexistent Reviews Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404