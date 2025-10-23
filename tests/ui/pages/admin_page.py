from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage
import allure


class AdminPage(BasePage):
    """Класс для работы с админской страницей"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.loading_text = "text=Loading..."
        self.meta_description = 'meta[name="description"]'
        self.meta_generator = 'meta[name="generator"]'
        self.login_form = 'form'  # Добавляем для проверки редиректа

    def navigate_to_admin(self):
        """Переход на админскую страницу (ожидаем редирект на логин)"""
        with allure.step("Переход на админскую страницу"):
            self.navigate("/admin")
            self.page.wait_for_load_state("networkidle")

            # После навигации ожидаем редирект на /login
            if "/login" in self.page.url:
                allure.attach(
                    "Автоматический редирект на страницу логина",
                    name="Redirect Info",
                    attachment_type=allure.attachment_type.TEXT
                )

    def verify_admin_redirect(self):
        """Проверка что админская страница перенаправляет на логин"""
        with allure.step("Проверка редиректа на страницу логина"):
            expect(self.page).to_have_url(self.base_url + "/login")

            # Проверяем что видна форма логина
            login_form = self.page.locator(self.login_form)
            expect(login_form).to_be_visible()

            allure.attach(
                "Редирект на страницу логина подтвержден",
                name="Redirect Verification",
                attachment_type=allure.attachment_type.TEXT
            )

    def is_loading_visible(self) -> bool:
        """Проверка видимости текста загрузки (после редиректа не актуально)"""
        try:
            return self.page.locator(self.loading_text).is_visible()
        except:
            return False

    def get_redirect_info(self) -> dict:
        """Получение информации о редиректе"""
        return {
            "current_url": self.page.url,
            "is_redirected_to_login": "/login" in self.page.url,
            "login_form_visible": self.page.locator(
                self.login_form).is_visible() if "/login" in self.page.url else False
        }