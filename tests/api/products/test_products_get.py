import pytest
import allure

@pytest.mark.api
@pytest.mark.products
@allure.feature("Products - GET")
@allure.severity(allure.severity_level.NORMAL)
class TestProductsGet:

    @allure.story("Получение товаров")
    @allure.description("Проверка получения всех товаров")
    @allure.tag("products", "get", "positive")
    def test_get_all_products(self, api_client):
        """GET /products - получить все товары"""
        with allure.step("Выполнить запрос на получение всех товаров"):
            response = api_client.get_products()
            allure.attach(f"Response: {response.status_code}",
                          name="Get Products Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "products" in data
            assert "total" in data
            assert isinstance(data["products"], list)
            assert len(data["products"]) > 0

        allure.attach(f"Total products: {data['total']}", name="Products Count",
                      attachment_type=allure.attachment_type.TEXT)

    @allure.story("Фильтрация товаров")
    @allure.description("Проверка фильтрации товаров по категории")
    @allure.tag("products", "get", "filter", "positive")
    def test_get_products_filter_by_category(self, api_client):
        """GET /products?category=Electronics - фильтрация по категории"""
        with allure.step("Выполнить запрос с фильтром по категории Electronics"):
            response = api_client.get_products({"category": "Electronics"})

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить что все товары в категории Electronics"):
            data = response.json()
            for product in data["products"]:
                assert product["category"] == "Electronics"

        allure.attach(f"Filtered products count: {len(data['products'])}",
                      name="Filtered Results",
                      attachment_type=allure.attachment_type.TEXT)

    @allure.story("Фильтрация товаров")
    @allure.description("Проверка фильтрации товаров по цене")
    @allure.tag("products", "get", "filter", "positive")
    def test_get_products_filter_by_price(self, api_client):
        """GET /products?minPrice=100&maxPrice=300 - фильтрация по цене"""
        with allure.step("Выполнить запрос с фильтром по цене 100-300"):
            response = api_client.get_products({
                "minPrice": 100,
                "maxPrice": 300
            })

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить что все товары в диапазоне цен 100-300"):
            data = response.json()
            for product in data["products"]:
                assert 100 <= product["price"] <= 300

    @allure.story("Поиск товаров")
    @allure.description("Проверка поиска товаров по ключевому слову")
    @allure.tag("products", "get", "search", "positive")
    def test_get_products_search(self, api_client):
        """GET /products?search=headphones - поиск товаров"""
        with allure.step("Выполнить поиск по ключевому слову 'headphones'"):
            response = api_client.get_products({"search": "headphones"})

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить что в названиях товаров есть 'headphone'"):
            data = response.json()
            for product in data["products"]:
                assert "headphone" in product["name"].lower()

    @allure.story("Невалидные фильтры")
    @allure.description("Проверка обработки невалидных параметров фильтрации")
    @allure.tag("products", "get", "filter", "negative", "validation")
    def test_get_products_invalid_filters(self, api_client):
        """GET /products - невалидные параметры фильтрации"""
        test_cases = [
            ("Отрицательная цена", {"minPrice": -10}),
            ("Инвертированный диапазон цен", {"minPrice": 500, "maxPrice": 100}),
            ("Несуществующая категория", {"category": "NonexistentCategory"}),
            ("Длинный поисковый запрос", {"search": "a" * 1000})
        ]

        for description, filters in test_cases:
            with allure.step(f"Проверить {description}"):
                response = api_client.get_products(filters)
                allure.attach(f"Filters: {filters}\nStatus: {response.status_code}",
                              name=f"{description} Response",
                              attachment_type=allure.attachment_type.TEXT)
                assert response.status_code == 200

    @allure.story("Получение одного товара")
    @allure.description("Проверка получения товара по ID")
    @allure.tag("products", "get", "positive")
    def test_get_single_product(self, api_client):
        """GET /products/{id} - получить товар по ID"""
        with allure.step("Получить список товаров и взять первый ID"):
            products_response = api_client.get_products()
            product_id = products_response.json()["products"][0]["id"]

        with allure.step(f"Получить товар по ID {product_id}"):
            response = api_client.get_product(product_id)
            allure.attach(f"Response: {response.status_code}",
                          name="Get Single Product Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить структуру ответа"):
            data = response.json()
            assert "product" in data
            assert data["product"]["id"] == product_id

    @allure.story("Получение несуществующего товара")
    @allure.description("Проверка ошибки при получении несуществующего товара")
    @allure.tag("products", "get", "negative")
    def test_get_nonexistent_product(self, api_client):
        """GET /products/{id} - несуществующий товар"""
        with allure.step("Попытаться получить несуществующий товар"):
            response = api_client.get_product("nonexistent-id")
            allure.attach(f"Response: {response.status_code}",
                          name="Get Nonexistent Response",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404
