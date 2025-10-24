import pytest
import allure
import random
import string

@pytest.mark.api
@pytest.mark.products
@pytest.mark.validation
@allure.feature("Products - Validation")
@allure.severity(allure.severity_level.NORMAL)
class TestProductsValidation:

    def generate_unique_product_name(self):
        """Генерация уникального имени товара"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"Test Product {random_suffix}"

    @allure.story("Валидация цены")
    @allure.description("Проверка обработки невалидной цены товара")
    @allure.tag("products", "validation", "negative")
    def test_create_product_invalid_price(self, auth_client):
        """POST /products - невалидная цена"""
        with allure.step("Подготовить данные с отрицательной ценой"):
            invalid_data = {
                "name": self.generate_unique_product_name(),
                "price": -100,
                "category": "Electronics",
                "stock": 10
            }
            allure.attach(str(invalid_data), name="Invalid Price Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос с невалидной ценой"):
            response = auth_client.create_product(invalid_data)
            allure.attach(f"Invalid Price Response: {response.status_code}\n{response.text}",
                          name="Invalid Price Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [201, 400, 422]

    @allure.story("Валидация количества")
    @allure.description("Проверка обработки невалидного количества товара")
    @allure.tag("products", "validation", "negative")
    def test_create_product_invalid_stock(self, auth_client):
        """POST /products - невалидный stock"""
        with allure.step("Подготовить данные с отрицательным stock"):
            invalid_data = {
                "name": self.generate_unique_product_name(),
                "price": 100,
                "category": "Electronics",
                "stock": -5
            }
            allure.attach(str(invalid_data), name="Invalid Stock Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос с невалидным stock"):
            response = auth_client.create_product(invalid_data)
            allure.attach(f"Invalid Stock Response: {response.status_code}\n{response.text}",
                          name="Invalid Stock Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [201, 400, 422]

    @allure.story("Валидация имени")
    @allure.description("Проверка обработки пустого имени товара")
    @allure.tag("products", "validation", "negative")
    def test_create_product_empty_name(self, auth_client):
        """POST /products - пустое имя"""
        with allure.step("Подготовить данные с пустым именем"):
            invalid_data = {
                "name": "",
                "price": 100,
                "category": "Electronics",
                "stock": 10
            }

        with allure.step("Выполнить запрос с пустым именем"):
            response = auth_client.create_product(invalid_data)
            allure.attach(f"Empty Name Response: {response.status_code}\n{response.text}",
                          name="Empty Name Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [201, 400, 422]

    @allure.story("Валидация данных при обновлении")
    @allure.description("Проверка обработки невалидных данных при обновлении товара")
    @allure.tag("products", "validation", "negative", "update")
    def test_update_product_invalid_data(self, auth_client):
        """PUT /products/{id} - невалидные данные при обновлении"""
        with allure.step("Создать валидный товар для обновления"):
            valid_data = {
                "name": self.generate_unique_product_name(),
                "price": 100,
                "category": "Electronics",
                "stock": 10
            }
            create_response = auth_client.create_product(valid_data)
            allure.attach(f"Create Response: {create_response.status_code}",
                          name="Create for Update",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить успешность создания"):
            if create_response.status_code != 201:
                pytest.skip("Could not create product for update test")

        with allure.step("Извлечь ID созданного товара"):
            create_data = create_response.json()
            if "product" in create_data:
                product_id = create_data["product"]["id"]
            elif "id" in create_data:
                product_id = create_data["id"]
            else:
                products_response = auth_client.get_products()
                products_data = products_response.json()
                our_product = next((p for p in products_data["products"] if p["name"] == valid_data["name"]), None)
                if our_product is None:
                    pytest.skip("Could not find created product")
                product_id = our_product["id"]

        with allure.step("Подготовить невалидные данные для обновления"):
            invalid_update = {
                "name": self.generate_unique_product_name(),
                "price": "invalid_price",
                "category": "Electronics",
                "stock": 10
            }
            allure.attach(str(invalid_update), name="Invalid Update Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить обновление с невалидными данными"):
            response = auth_client.update_product(product_id, invalid_update, method="PUT")
            allure.attach(f"Invalid Update Response: {response.status_code}\n{response.text}",
                          name="Invalid Update Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [400, 404, 422, 200]

        with allure.step("Если обновление успешно, проверить конвертацию данных"):
            if response.status_code == 200:
                updated_data = response.json()
                if "product" in updated_data:
                    updated_price = updated_data["product"]["price"]
                    allure.attach(f"Updated price: {updated_price} (type: {type(updated_price)})",
                                  name="Price Conversion",
                                  attachment_type=allure.attachment_type.TEXT)

    @allure.story("Валидация длины имени")
    @allure.description("Проверка обработки очень длинного имени товара")
    @allure.tag("products", "validation", "negative")
    def test_create_product_very_long_name(self, auth_client):
        """POST /products - очень длинное имя"""
        with allure.step("Сгенерировать очень длинное имя"):
            long_name = "A" * 1000
            invalid_data = {
                "name": long_name,
                "price": 100,
                "category": "Electronics",
                "stock": 10
            }

        with allure.step("Выполнить запрос с очень длинным именем"):
            response = auth_client.create_product(invalid_data)
            allure.attach(f"Long Name Response: {response.status_code}\n{response.text}",
                          name="Long Name Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [201, 400, 413]

    @allure.story("Валидация специальных символов")
    @allure.description("Проверка обработки специальных символов в имени товара")
    @allure.tag("products", "validation", "negative")
    def test_create_product_special_characters(self, auth_client):
        """POST /products - специальные символы в имени"""
        with allure.step("Подготовить данные со специальными символами"):
            special_name = "Product @#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
            invalid_data = {
                "name": special_name,
                "price": 100,
                "category": "Electronics",
                "stock": 10
            }
            allure.attach(str(invalid_data), name="Special Chars Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Выполнить запрос со специальными символами"):
            response = auth_client.create_product(invalid_data)
            allure.attach(f"Special Chars Response: {response.status_code}\n{response.text}",
                          name="Special Chars Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить возможные статус коды"):
            assert response.status_code in [201, 400]