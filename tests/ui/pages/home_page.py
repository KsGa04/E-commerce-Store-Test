from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage
import allure


class HomePage(BasePage):
    """Класс для работы с главной страницей"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.meta_description = 'meta[name="description"]'
        self.meta_generator = 'meta[name="generator"]'
        self.meta_viewport = 'meta[name="viewport"]'

    def navigate_to_home(self):
        """Переход на главную страницу"""
        with allure.step("Переход на главную страницу"):
            self.navigate("/")
            self.page.wait_for_load_state("networkidle")

    def verify_home_page_loaded(self):
        """Проверка загрузки главной страницы"""
        with allure.step("Проверка загрузки главной страницы"):
            expect(self.page).to_have_title("v0 App")

            meta_description = self.page.locator(self.meta_description)
            expect(meta_description).to_have_attribute("content", "Created with v0")

            allure.attach("Главная страница загружена успешно", name="Page Load",
                          attachment_type=allure.attachment_type.TEXT)

    def verify_home_page_accessible(self):
        """Проверка что главная страница доступна"""
        with allure.step("Проверка доступности главной страницы"):
            expect(self.page).to_have_url(self.base_url + "/")
            expect(self.page.locator("body")).to_be_visible()

            # Проверяем что есть какой-то контент
            body_content = self.page.locator("body").text_content()
            assert body_content is not None and len(body_content) > 0, "Страница должна содержать контент"

            allure.attach("Главная страница доступна и содержит контент", name="Page Access",
                          attachment_type=allure.attachment_type.TEXT)

    def get_page_info(self) -> dict:
        """Получение информации о странице"""
        return {
            "url": self.page.url,
            "title": self.page.title(),
            "has_content": len(self.page.locator("body").text_content() or "") > 0
        }