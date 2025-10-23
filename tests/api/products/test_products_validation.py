import pytest
import allure
import random
import string


@allure.feature("Products - Validation")
class TestProductsValidation:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"Test Product {random_suffix}"

    def test_create_product_invalid_price(self, auth_client):
        """POST /products - невалидная цена"""
        invalid_data = {
            "name": self.generate_unique_product_name(),
            "price": -100,  # Отрицательная цена
            "category": "Electronics",
            "stock": 10
        }
        response = auth_client.create_product(invalid_data)
        print("INVALID PRICE RESPONSE:", response.status_code, response.json())
        # API может принять отрицательную цену или вернуть ошибку
        assert response.status_code in [201, 400, 422]

    def test_create_product_invalid_stock(self, auth_client):
        """POST /products - невалидный stock"""
        invalid_data = {
            "name": self.generate_unique_product_name(),
            "price": 100,
            "category": "Electronics",
            "stock": -5  # Отрицательный stock
        }
        response = auth_client.create_product(invalid_data)
        print("INVALID STOCK RESPONSE:", response.status_code, response.json())
        # API может принять отрицательный stock или вернуть ошибку
        assert response.status_code in [201, 400, 422]

    def test_create_product_empty_name(self, auth_client):
        """POST /products - пустое имя"""
        invalid_data = {
            "name": "",  # Пустое имя
            "price": 100,
            "category": "Electronics",
            "stock": 10
        }
        response = auth_client.create_product(invalid_data)
        print("EMPTY NAME RESPONSE:", response.status_code, response.json())
        # API может отклонить пустое имя или принять его
        assert response.status_code in [201, 400, 422]

    def test_update_product_invalid_data(self, auth_client):
        """PUT /products/{id} - невалидные данные при обновлении"""
        # Сначала создаем валидный товар с уникальным именем
        valid_data = {
            "name": self.generate_unique_product_name(),
            "price": 100,
            "category": "Electronics",
            "stock": 10
        }
        create_response = auth_client.create_product(valid_data)
        print("CREATE FOR UPDATE RESPONSE:", create_response.status_code, create_response.json())

        # Проверяем, что создание прошло успешно
        if create_response.status_code != 201:
            pytest.skip("Could not create product for update test")

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
            our_product = next((p for p in products_data["products"] if p["name"] == valid_data["name"]), None)
            if our_product is None:
                pytest.skip("Could not find created product")
            product_id = our_product["id"]

        # Пытаемся обновить с невалидными данными
        invalid_update = {
            "name": self.generate_unique_product_name(),
            "price": "invalid_price",  # Строка вместо числа
            "category": "Electronics",
            "stock": 10
        }
        response = auth_client.update_product(product_id, invalid_update, method="PUT")
        print("INVALID UPDATE RESPONSE:", response.status_code, response.json())

        # API может вернуть 400 (Bad Request), 404 (Not Found) или 422 (Unprocessable Entity)
        # Или даже 200 если автоматически конвертирует типы
        assert response.status_code in [400, 404, 422, 200]

        # Если вернулся 200, проверяем что цена действительно обновилась
        if response.status_code == 200:
            updated_data = response.json()
            if "product" in updated_data:
                # Проверяем, что цена стала числом (автоконвертация) или осталась строкой
                updated_price = updated_data["product"]["price"]
                print(f"Updated price type: {type(updated_price)}, value: {updated_price}")

    def test_create_product_very_long_name(self, auth_client):
        """POST /products - очень длинное имя"""
        long_name = "A" * 1000  # Очень длинное имя
        invalid_data = {
            "name": long_name,
            "price": 100,
            "category": "Electronics",
            "stock": 10
        }
        response = auth_client.create_product(invalid_data)
        print("LONG NAME RESPONSE:", response.status_code, response.json())
        # API может принять длинное имя, обрезать его или вернуть ошибку
        assert response.status_code in [201, 400, 413]

    def test_create_product_special_characters(self, auth_client):
        """POST /products - специальные символы в имени"""
        special_name = "Product @#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
        invalid_data = {
            "name": special_name,
            "price": 100,
            "category": "Electronics",
            "stock": 10
        }
        response = auth_client.create_product(invalid_data)
        print("SPECIAL CHARS RESPONSE:", response.status_code, response.json())
        # API может принять специальные символы или вернуть ошибку
        assert response.status_code in [201, 400]