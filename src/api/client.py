import requests
from config.environment import Environment


class ApiClient:
    def __init__(self):
        self.base_url = Environment.API_URL
        self.session = requests.Session()
        self.token = None

    def login(self, username, password):
        """Логин и сохранение токена"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
            if self.token:
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                })

        return response

    def get_products(self, filters=None):
        """Получить список товаров"""
        return self.session.get(
            f"{self.base_url}/products",
            params=filters or {}
        )

    def get_product(self, product_id):
        """Получить товар по ID"""
        return self.session.get(f"{self.base_url}/products/{product_id}")

    def create_product(self, product_data):
        """Создать новый товар (требует авторизации)"""
        return self.session.post(
            f"{self.base_url}/products",
            json=product_data
        )

    def update_product(self, product_id, product_data, method="PUT"):
        """Обновить товар (PUT - полное, PATCH - частичное)"""
        if method.upper() == "PUT":
            return self.session.put(
                f"{self.base_url}/products/{product_id}",
                json=product_data
            )
        elif method.upper() == "PATCH":
            return self.session.patch(
                f"{self.base_url}/products/{product_id}",
                json=product_data
            )

    def delete_product(self, product_id):
        """Удалить товар (требует авторизации)"""
        return self.session.delete(f"{self.base_url}/products/{product_id}")

    def get_categories(self):
        """Получить список категорий"""
        return self.session.get(f"{self.base_url}/categories")

    def get_reviews(self, product_id):
        """Получить отзывы о товаре"""
        return self.session.get(f"{self.base_url}/products/{product_id}/review")

    def create_review(self, product_id, review_data):
        """Добавить отзыв (требует авторизации)"""
        return self.session.post(
            f"{self.base_url}/products/{product_id}/review",
            json=review_data
        )