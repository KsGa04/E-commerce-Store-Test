import pytest
from src.api.client import ApiClient
from config.environment import Environment


class TestProductsCRUD:
    @pytest.fixture
    def auth_client(self):
        """Фикстура для авторизованного клиента"""
        client = ApiClient()
        client.login(
            Environment.TEST_USER["username"],
            Environment.TEST_USER["password"]
        )
        return client

    @pytest.fixture
    def sample_product(self):
        """Фикстура с тестовыми данными товара"""
        return {
            "name": "Test Gaming Keyboard",
            "description": "Mechanical gaming keyboard with RGB",
            "price": 129.99,
            "category": "Electronics",
            "stock": 25,
            "imageUrl": "/keyboard.png"
        }

    def test_create_product(self, auth_client, sample_product):
        """Тест создания товара"""
        response = auth_client.create_product(sample_product)

        # Должен вернуть 201 Created согласно документации
        assert response.status_code == 201

        data = response.json()
        print("CREATE RESPONSE:", data)  # Отладочная информация

        # Согласно реальному API, при создании товара может возвращаться просто сообщение
        # или объект с product. Проверяем оба варианта.
        if "product" in data:
            created_product = data["product"]
        elif "message" in data:
            # Если возвращается только сообщение, нам нужно получить ID другим способом
            # Например, через список товаров
            products_response = auth_client.get_products()
            products_data = products_response.json()
            # Найдем наш созданный товар по имени
            our_product = next((p for p in products_data["products"] if p["name"] == sample_product["name"]), None)
            assert our_product is not None, "Созданный товар не найден в списке"
            created_product = our_product
        else:
            # Если структура неизвестна, считаем что ответ и есть продукт
            created_product = data

        # Проверяем, что все поля совпадают
        assert created_product["name"] == sample_product["name"]
        assert created_product["price"] == sample_product["price"]
        assert created_product["category"] == sample_product["category"]
        assert created_product["stock"] == sample_product["stock"]
        assert "id" in created_product

        return created_product["id"]

    def test_update_product_put(self, auth_client, sample_product):
        """Тест полного обновления товара (PUT)"""
        # Сначала создаем товар
        create_response = auth_client.create_product(sample_product)
        product_id = self._extract_product_id(create_response, sample_product["name"], auth_client)

        # Данные для полного обновления (все поля обязательны для PUT)
        update_data = {
            "name": "Updated Gaming Keyboard",
            "description": "Updated description",
            "price": 149.99,
            "category": "Electronics",
            "stock": 30,
            "imageUrl": "/updated-keyboard.png"
        }

        def test_put_requires_all_fields(self, auth_client, sample_product):
            """Тест, что PUT требует все обязательные поля"""
            # Сначала создаем товар
            create_response = auth_client.create_product(sample_product)
            product_id = self._extract_product_id(create_response, sample_product["name"], auth_client)

            # Пытаемся обновить с отсутствующими обязательными полями
            incomplete_data = {
                "name": "Updated Product",
                "price": 199.99
                # Отсутствуют category, stock и другие обязательные поля
            }

            response = auth_client.update_product(product_id, incomplete_data, method="PUT")
            print("PUT VALIDATION RESPONSE:", response.json())  # Отладочная информация
            assert response.status_code == 400

            error_data = response.json()
            assert "error" in error_data
            assert "required" in error_data

        response = auth_client.update_product(product_id, update_data, method="PUT")
        print("PUT UPDATE RESPONSE:", response.json())  # Отладочная информация
        assert response.status_code == 200

        updated_data = response.json()
        # Согласно скриншоту, ответ содержит message и product
        assert "message" in updated_data
        assert "product" in updated_data
        updated_product = updated_data["product"]
        assert updated_product["name"] == update_data["name"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["stock"] == update_data["stock"]

    def test_update_product_patch(self, auth_client, sample_product):
        """Тест частичного обновления товара (PATCH)"""
        # Сначала создаем товар
        create_response = auth_client.create_product(sample_product)
        product_id = self._extract_product_id(create_response, sample_product["name"], auth_client)

        # Данные для частичного обновления (поля опциональны для PATCH)
        patch_data = {
            "price": 119.99,
            "stock": 15
        }

        response = auth_client.update_product(product_id, patch_data, method="PATCH")
        print("PATCH UPDATE RESPONSE:", response.json())  # Отладочная информация
        assert response.status_code == 200

        updated_data = response.json()
        # Согласно скриншоту, ответ содержит message и product
        assert "message" in updated_data
        assert "product" in updated_data
        updated_product = updated_data["product"]
        # Проверяем обновленные поля
        assert updated_product["price"] == patch_data["price"]
        assert updated_product["stock"] == patch_data["stock"]
        # Проверяем, что остальные поля не изменились
        assert updated_product["name"] == sample_product["name"]
        assert updated_product["category"] == sample_product["category"]

    def test_delete_product(self, auth_client, sample_product):
        """Тест удаления товара"""
        # Сначала создаем товар
        create_response = auth_client.create_product(sample_product)
        product_id = self._extract_product_id(create_response, sample_product["name"], auth_client)

        # Удаляем товар
        delete_response = auth_client.delete_product(product_id)
        print("DELETE RESPONSE:", delete_response.json())  # Отладочная информация
        assert delete_response.status_code == 200

        # Проверяем, что товар действительно удален
        get_response = auth_client.get_product(product_id)
        assert get_response.status_code == 404

    def test_unauthorized_access(self):
        """Тест попытки доступа к защищенным endpoints без авторизации"""
        client = ApiClient()  # Не авторизован

        sample_product = {
            "name": "Test Product",
            "price": 100.0,
            "category": "Test",
            "stock": 10
        }

        # Попытка создать товар без авторизации
        response = client.create_product(sample_product)
        assert response.status_code == 401

    def test_create_product_duplicate_name(self, auth_client):
        """Тест создания товара с существующим именем (должен вернуть 409)"""
        sample_product = {
            "name": "Duplicate Product",
            "description": "Test duplicate",
            "price": 100.0,
            "category": "Test",
            "stock": 10
        }

        # Первое создание - должно быть успешно
        response1 = auth_client.create_product(sample_product)
        assert response1.status_code == 201

        # Второе создание с тем же именем - должно вернуть 409
        response2 = auth_client.create_product(sample_product)
        assert response2.status_code == 409

    def _extract_product_id(self, create_response, product_name, auth_client):
        """Вспомогательный метод для извлечения ID созданного товара"""
        data = create_response.json()

        if "product" in data:
            return data["product"]["id"]
        elif "id" in data:
            return data["id"]
        else:
            # Если ID нет в ответе, ищем товар по имени в списке
            products_response = auth_client.get_products()
            products_data = products_response.json()
            our_product = next((p for p in products_data["products"] if p["name"] == product_name), None)
            assert our_product is not None, f"Товар с именем '{product_name}' не найден в списке"
            return our_product["id"]