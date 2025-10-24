import pytest
import allure
import random
import string

@pytest.mark.api
@pytest.mark.integrations
@pytest.mark.workflows
@allure.feature("Integration Workflows")
@allure.severity(allure.severity_level.CRITICAL)
class TestWorkflows:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"Test Product {random_suffix}"

    @allure.story("Полный жизненный цикл товара")
    @allure.description("Тест полного цикла работы с товаром: создание -> обновление -> удаление")
    @allure.tag("workflow", "lifecycle", "integration")
    def test_full_product_lifecycle(self, auth_client):
        """Полный цикл работы с товаром: создание -> обновление -> удаление"""

        with allure.step("1. Создание товара"):
            product_data = {
                "name": self.generate_unique_product_name(),
                "description": "Test description",
                "price": 100.0,
                "category": "Electronics",
                "stock": 10
            }
            allure.attach(str(product_data), name="Product Data", attachment_type=allure.attachment_type.JSON)

            create_response = auth_client.create_product(product_data)
            allure.attach(f"Create Response: {create_response.status_code}",
                          name="Create Product Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert create_response.status_code == 201

        with allure.step("Извлечь ID созданного товара"):
            create_data = create_response.json()
            if "product" in create_data:
                product_id = create_data["product"]["id"]
            elif "id" in create_data:
                product_id = create_data["id"]
            else:
                products_response = auth_client.get_products()
                products_data = products_response.json()
                our_product = next((p for p in products_data["products"] if p["name"] == product_data["name"]), None)
                assert our_product is not None
                product_id = our_product["id"]

            allure.attach(f"Product ID: {product_id}", name="Product ID", attachment_type=allure.attachment_type.TEXT)

        with allure.step("2. Чтение товара"):
            get_response = auth_client.get_product(product_id)
            assert get_response.status_code == 200

        with allure.step("3. Частичное обновление (PATCH)"):
            patch_response = auth_client.update_product(product_id, {"price": 150.0}, method="PATCH")
            allure.attach(f"PATCH Response: {patch_response.status_code}",
                          name="PATCH Update Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert patch_response.status_code == 200

        with allure.step("4. Полное обновление (PUT)"):
            update_data = {
                "name": self.generate_unique_product_name(),
                "description": "Updated description",
                "price": 200.0,
                "category": "Home",
                "stock": 20
            }
            allure.attach(str(update_data), name="PUT Update Data", attachment_type=allure.attachment_type.JSON)

            put_response = auth_client.update_product(product_id, update_data, method="PUT")
            allure.attach(f"PUT Response: {put_response.status_code}",
                          name="PUT Update Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert put_response.status_code == 200

        with allure.step("5. Добавление отзыва"):
            review_data = {
                "rating": 5,
                "comment": "Great product!",
                "author": "Integration Test User"
            }
            review_response = auth_client.create_review(product_id, review_data)
            allure.attach(f"Review Response: {review_response.status_code}",
                          name="Create Review Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert review_response.status_code == 201

        with allure.step("6. Проверка отзывов"):
            reviews_response = auth_client.get_reviews(product_id)
            assert reviews_response.status_code == 200

        with allure.step("7. Удаление товара"):
            delete_response = auth_client.delete_product(product_id)
            allure.attach(f"Delete Response: {delete_response.status_code}",
                          name="Delete Product Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert delete_response.status_code == 200

        with allure.step("8. Проверка удаления"):
            final_get_response = auth_client.get_product(product_id)
            assert final_get_response.status_code == 404

    @allure.story("Работа с отзывами")
    @allure.description("Тест работы с товаром и отзывами")
    @allure.tag("workflow", "reviews", "integration")
    def test_product_with_reviews_workflow(self, auth_client):
        """Работа с товаром и отзывами"""
        with allure.step("Создать товар"):
            product_data = {
                "name": self.generate_unique_product_name(),
                "price": 50.0,
                "category": "Electronics",
                "stock": 5
            }
            create_response = auth_client.create_product(product_data)
            allure.attach(f"Create Response: {create_response.status_code}",
                          name="Create Product Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert create_response.status_code == 201

        with allure.step("Извлечь ID товара"):
            create_data = create_response.json()
            if "product" in create_data:
                product_id = create_data["product"]["id"]
            elif "id" in create_data:
                product_id = create_data["id"]
            else:
                products_response = auth_client.get_products()
                products_data = products_response.json()
                our_product = next((p for p in products_data["products"] if p["name"] == product_data["name"]), None)
                assert our_product is not None
                product_id = our_product["id"]

        with allure.step("Получить начальные отзывы"):
            initial_reviews_response = auth_client.get_reviews(product_id)
            assert initial_reviews_response.status_code == 200
            initial_reviews_count = len(initial_reviews_response.json()["reviews"])
            allure.attach(f"Initial reviews count: {initial_reviews_count}",
                          name="Initial Reviews",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Добавить несколько отзывов"):
            reviews_to_add = [
                {"rating": 5, "comment": "Excellent!", "author": "User1"},
                {"rating": 4, "comment": "Very good", "author": "User2"},
                {"rating": 3, "comment": "Average", "author": "User3"}
            ]

            for i, review in enumerate(reviews_to_add):
                with allure.step(f"Добавить отзыв {i + 1}"):
                    response = auth_client.create_review(product_id, review)
                    allure.attach(f"Review {i + 1} Response: {response.status_code}",
                                  name=f"Review {i + 1} Response",
                                  attachment_type=allure.attachment_type.TEXT)
                    assert response.status_code == 201

        with allure.step("Проверить добавление отзывов"):
            final_reviews_response = auth_client.get_reviews(product_id)
            assert final_reviews_response.status_code == 200
            final_reviews = final_reviews_response.json()["reviews"]

            expected_count = initial_reviews_count + len(reviews_to_add)
            allure.attach(f"Expected: {expected_count}, Actual: {len(final_reviews)}",
                          name="Reviews Count Check",
                          attachment_type=allure.attachment_type.TEXT)
            assert len(final_reviews) == expected_count, f"Expected {expected_count} reviews, got {len(final_reviews)}"

        with allure.step("Очистка - удалить товар"):
            delete_response = auth_client.delete_product(product_id)
            allure.attach(f"Cleanup Delete Response: {delete_response.status_code}",
                          name="Cleanup Response",
                          attachment_type=allure.attachment_type.TEXT)
            assert delete_response.status_code == 200