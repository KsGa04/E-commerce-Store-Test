import pytest
import allure
import random
import string


@allure.feature("Integration Workflows")
class TestWorkflows:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"Test Product {random_suffix}"

    def test_full_product_lifecycle(self, auth_client):
        """Полный цикл работы с товаром: создание -> обновление -> удаление"""
        # 1. Создание
        product_data = {
            "name": self.generate_unique_product_name(),
            "description": "Test description",
            "price": 100.0,
            "category": "Electronics",
            "stock": 10
        }
        create_response = auth_client.create_product(product_data)
        assert create_response.status_code == 201

        # Извлекаем ID товара
        create_data = create_response.json()
        if "product" in create_data:
            product_id = create_data["product"]["id"]
        elif "id" in create_data:
            product_id = create_data["id"]
        else:
            # Если ID нет в ответе, ищем в списке
            products_response = auth_client.get_products()
            products_data = products_response.json()
            our_product = next((p for p in products_data["products"] if p["name"] == product_data["name"]), None)
            assert our_product is not None
            product_id = our_product["id"]

        # 2. Чтение
        get_response = auth_client.get_product(product_id)
        assert get_response.status_code == 200

        # 3. Обновление (PATCH)
        patch_response = auth_client.update_product(product_id, {"price": 150.0}, method="PATCH")
        assert patch_response.status_code == 200

        # 4. Обновление (PUT)
        update_data = {
            "name": self.generate_unique_product_name(),
            "description": "Updated description",
            "price": 200.0,
            "category": "Home",
            "stock": 20
        }
        put_response = auth_client.update_product(product_id, update_data, method="PUT")
        assert put_response.status_code == 200

        # 5. Добавление отзыва
        review_data = {
            "rating": 5,
            "comment": "Great product!",
            "author": "Integration Test User"
        }
        review_response = auth_client.create_review(product_id, review_data)
        assert review_response.status_code == 201

        # 6. Проверка отзывов
        reviews_response = auth_client.get_reviews(product_id)
        assert reviews_response.status_code == 200

        # 7. Удаление
        delete_response = auth_client.delete_product(product_id)
        assert delete_response.status_code == 200

        # 8. Проверка удаления
        final_get_response = auth_client.get_product(product_id)
        assert final_get_response.status_code == 404

    def test_product_with_reviews_workflow(self, auth_client):
        """Работа с товаром и отзывами"""
        # Создаем товар
        product_data = {
            "name": self.generate_unique_product_name(),
            "price": 50.0,
            "category": "Electronics",
            "stock": 5
        }
        create_response = auth_client.create_product(product_data)
        assert create_response.status_code == 201

        # Извлекаем ID товара
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

        # Получаем текущие отзывы (чтобы знать исходное количество)
        initial_reviews_response = auth_client.get_reviews(product_id)
        assert initial_reviews_response.status_code == 200
        initial_reviews_count = len(initial_reviews_response.json()["reviews"])

        # Добавляем несколько отзывов
        reviews_to_add = [
            {"rating": 5, "comment": "Excellent!", "author": "User1"},
            {"rating": 4, "comment": "Very good", "author": "User2"},
            {"rating": 3, "comment": "Average", "author": "User3"}
        ]

        for review in reviews_to_add:
            response = auth_client.create_review(product_id, review)
            assert response.status_code == 201

        # Проверяем, что отзывы добавились
        final_reviews_response = auth_client.get_reviews(product_id)
        assert final_reviews_response.status_code == 200
        final_reviews = final_reviews_response.json()["reviews"]

        # Должно быть initial + добавленные отзывы
        expected_count = initial_reviews_count + len(reviews_to_add)
        assert len(final_reviews) == expected_count, f"Expected {expected_count} reviews, got {len(final_reviews)}"

        # Очистка
        delete_response = auth_client.delete_product(product_id)
        assert delete_response.status_code == 200