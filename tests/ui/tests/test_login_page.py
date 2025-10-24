import pytest
from playwright.sync_api import expect
import time


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
class TestLoginPage:
    """Тесты для страницы логина"""

    def test_login_page_structure(self, login_page):
        """Тест структуры страницы логина"""
        login_page.navigate_to_login()
        login_page.verify_login_page_structure()
        login_page.verify_form_elements()

    def test_login_with_valid_credentials(self, login_page):
        """Тест логина с валидными credentials"""
        login_page.navigate_to_login()

        # Делаем скриншот до логина
        login_page.take_screenshot("before_login")

        login_page.login_with_valid_credentials()

        # Делаем скриншот после логина
        login_page.take_screenshot("after_login")

        # Выводим отладочную информацию
        print(f"Current URL: {login_page.page.url}")
        print(f"Page title: {login_page.page.title()}")

        # Проверяем редирект
        is_successful = login_page.is_login_successful()

        if not is_successful:
            # Дополнительная диагностика
            print("Login failed. Diagnostic info:")
            print(f"URL contains '/login': {'/login' in login_page.page.url}")
            print(f"Login form visible: {login_page.page.locator(login_page.login_form).is_visible()}")
            print(f"Error message: {login_page.get_error_message()}")

        assert is_successful, "Login should be successful with valid credentials"

    def test_login_with_invalid_credentials(self, login_page):
        """Тест логина с невалидными credentials"""
        login_page.navigate_to_login()
        login_page.login_with_invalid_credentials()

        # Проверяем, что остались на странице логина
        assert login_page.is_login_failed(), "Should stay on login page with invalid credentials"

    def test_form_validation(self, login_page):
        """Тест валидации формы"""
        login_page.navigate_to_login()

        # Пытаемся отправить пустую форму
        login_button = login_page.page.locator(login_page.login_button)
        login_button.click()

        # Проверяем, что остались на странице
        expect(login_page.page).to_have_url(login_page.base_url + "/login")

        # Проверяем, что поля все еще пустые
        username_input = login_page.page.locator(login_page.username_input)
        password_input = login_page.page.locator(login_page.password_input)
        expect(username_input).to_have_value("")
        expect(password_input).to_have_value("")

    @pytest.mark.regression
    def test_responsive_design(self, login_page):
        """Тест адаптивного дизайна"""
        login_page.page.set_viewport_size({"width": 375, "height": 667})
        login_page.navigate_to_login()

        # Проверяем, что форма все еще видима и доступна
        card = login_page.page.locator('[data-slot="card"]')
        expect(card).to_be_visible()

        # Проверяем, что кнопка логина кликабельна
        login_button = login_page.page.locator(login_page.login_button)
        expect(login_button).to_be_enabled()