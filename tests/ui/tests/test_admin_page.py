import pytest
from playwright.sync_api import expect
import allure

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.admin
class TestAdminPage:
    """Тесты для админской страницы"""

    def test_admin_page_redirects_to_login(self, admin_page):
        """Тест что админская страница перенаправляет на логин"""
        with allure.step("Переход на админскую страницу"):
            admin_page.navigate_to_admin()

        with allure.step("Проверка редиректа на страницу логина"):
            admin_page.verify_admin_redirect()

    def test_admin_page_access_requires_login(self, admin_page, login_page):
        """Тест что доступ к админке требует аутентификации"""
        with allure.step("Попытка доступа к админской странице без логина"):
            admin_page.navigate_to_admin()

        with allure.step("Проверка что мы на странице логина"):
            expect(login_page.page).to_have_url(login_page.base_url + "/login")

            username_input = login_page.page.locator(login_page.username_input)
            password_input = login_page.page.locator(login_page.password_input)
            expect(username_input).to_be_visible()
            expect(password_input).to_be_visible()

            allure.attach(
                "Доступ к админке требует аутентификации",
                name="Authentication Required",
                attachment_type=allure.attachment_type.TEXT
            )

    def test_admin_page_meta_info(self, admin_page):
        """Тест мета-информации (после редиректа)"""
        admin_page.navigate_to_admin()

        with allure.step("Проверка мета-информации после редиректа"):
            expect(admin_page.page).to_have_title("v0 App")

            meta_description = admin_page.page.locator('meta[name="description"]')
            expect(meta_description).to_have_attribute("content", "Created with v0")

            allure.attach(
                "Мета-информация проверена успешно",
                name="Meta Info",
                attachment_type=allure.attachment_type.TEXT
            )

    @pytest.mark.regression
    def test_admin_redirect_responsive(self, admin_page):
        """Тест адаптивности редиректа с админской страницы"""
        with allure.step("Установка мобильного размера экрана"):
            admin_page.page.set_viewport_size({"width": 375, "height": 667})

        admin_page.navigate_to_admin()

        with allure.step("Проверка редиректа на мобильном устройстве"):
            expect(admin_page.page).to_have_url(admin_page.base_url + "/login")

            login_form = admin_page.page.locator(admin_page.login_form)
            expect(login_form).to_be_visible()

            admin_page.take_screenshot("admin_redirect_mobile")

            allure.attach(
                "Редирект на мобильном устройстве работает корректно",
                name="Mobile Redirect",
                attachment_type=allure.attachment_type.TEXT
            )