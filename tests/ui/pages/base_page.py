from playwright.sync_api import Page, expect
from tests.ui.utills.helpers import Helpers
import allure
import time


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, page: Page):
        self.page = page
        self.helpers = Helpers()
        self.base_url = "https://v0-swagger-backend-frontend.vercel.app"

    def navigate(self, url: str = ""):
        """Навигация на указанный URL"""
        full_url = f"{self.base_url}{url}"

        with allure.step(f"Переход на страницу: {full_url}"):
            self.page.goto(full_url, wait_until="networkidle", timeout=30000)

            # Прикрепляем URL к отчету
            allure.attach(
                f"Navigated to: {full_url}",
                name="Navigation Info",
                attachment_type=allure.attachment_type.TEXT
            )

    def get_title(self) -> str:
        """Получение заголовка страницы"""
        return self.page.title()

    def wait_for_element(self, selector: str, timeout: int = 15000):
        """Ожидание элемента"""
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")

    def click_element(self, selector: str, element_name: str = "элемент"):
        """Клик по элементу"""
        with allure.step(f"Клик на {element_name}"):
            self.page.click(selector)

    def fill_field(self, selector: str, value: str, field_name: str = "поле"):
        """Заполнение поля"""
        with allure.step(f"Заполнение {field_name}: {value}"):
            self.page.fill(selector, value)

    def take_screenshot(self, name: str):
        """Создание скриншота и прикрепление к Allure"""
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=f"screenshot_{name}",
            attachment_type=allure.attachment_type.PNG
        )
        return f"screenshot_{name}.png"

    def verify_page_loaded(self):
        """Базовая проверка загрузки страницы"""
        with allure.step("Проверка загрузки страницы"):
            expect(self.page).not_to_have_url("about:blank")
            self.page.wait_for_load_state("domcontentloaded")

            allure.attach(
                f"Page URL: {self.page.url}\nPage Title: {self.page.title()}",
                name="Page Info",
                attachment_type=allure.attachment_type.TEXT
            )