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
            # Добавляем токен в заголовки для последующих запросов
            if self.token:
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })

        return response

    def get_products(self, filters=None):
        """Получить список товаров"""
        return self.session.get(
            f"{self.base_url}/products",
            params=filters or {}
        )