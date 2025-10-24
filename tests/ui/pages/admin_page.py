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
        self.login_form = 'form'
        self.admin_panel_selector = "text=Admin Panel"  # Добавляем селектор для админки

    def navigate_to_admin(self):
        """Переход на админскую страницу (ожидаем редирект на логин)"""
        with allure.step("Переход на админскую страницу"):
            self.navigate("/admin")
            self.page.wait_for_load_state("networkidle")

            # Ждем либо редирект на логин, либо загрузку админки
            try:
                self.page.wait_for_url("**/login", timeout=5000)
                allure.attach(
                    "Автоматический редирект на страницу логина",
                    name="Redirect Info",
                    attachment_type=allure.attachment_type.TEXT
                )
            except:
                # Если нет редиректа, значит мы в админке
                allure.attach(
                    "Прямой доступ к админской странице",
                    name="Direct Access",
                    attachment_type=allure.attachment_type.TEXT
                )

    def verify_admin_redirect(self):
        """Проверка что админская страница перенаправляет на логин"""
        with allure.step("Проверка редиректа на страницу логина"):
            expect(self.page).to_have_url(self.base_url + "/login")

            login_form = self.page.locator(self.login_form)
            expect(login_form).to_be_visible()

            allure.attach(
                "Редирект на страницу логина подтвержден",
                name="Redirect Verification",
                attachment_type=allure.attachment_type.TEXT
            )

    def is_admin_page_loaded(self) -> bool:
        """Проверка загрузки админской страницы (после успешного логина)"""
        try:
            # Ждем либо элементы админки, либо остаемся на логине
            self.page.wait_for_timeout(2000)

            if "/admin" in self.page.url:
                # Проверяем наличие элементов админки
                admin_elements = [
                    "text=Admin",
                    "text=Dashboard",
                    "text=Panel"
                ]

                for selector in admin_elements:
                    if self.page.locator(selector).count() > 0:
                        return True
            return False
        except:
            return False

    def is_loading_visible(self) -> bool:
        """Проверка видимости текста загрузки - обновленная версия"""
        try:
            # Увеличиваем таймаут и делаем проверку более стабильной
            return self.page.locator(self.loading_text).is_visible(timeout=3000)
        except:
            return False

    def get_redirect_info(self) -> dict:
        """Получение информации о редиректе"""
        return {
            "current_url": self.page.url,
            "is_redirected_to_login": "/login" in self.page.url,
            "is_admin_page": "/admin" in self.page.url,
            "login_form_visible": self.page.locator(
                self.login_form).is_visible() if "/login" in self.page.url else False
        }