import pytest
import allure

@pytest.mark.api
@pytest.mark.categories
@allure.feature("Categories - GET")
@allure.severity(allure.severity_level.NORMAL)
class TestCategoriesGet:

    @allure.story("Получение категорий")
    @allure.description("Проверка успешного получения списка категорий")
    @allure.tag("categories", "get", "positive")
    def test_get_categories_success(self, api_client):
        """GET /categories - получить список категорий"""
        with allure.step("Выполнить запрос на получение категорий"):
            response = api_client.get_categories()

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "categories" in data
            assert "total" in data

        with allure.step("Проверить содержимое категорий"):
            categories = data["categories"]
            assert isinstance(categories, list)
            assert len(categories) > 0
            assert "Electronics" in categories
            assert "Home" in categories

        allure.attach(str(categories), name="Categories List", attachment_type=allure.attachment_type.JSON)