import pytest
from playwright.sync_api import expect
import allure

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
class TestNavigation:
    """Тесты навигации между страницами"""

    def test_navigation_between_pages(self, home_page, login_page, admin_page):
        """Тест навигации между всеми страницами с учетом редиректов"""
        with allure.step("1. Переход на главную страницу"):
            home_page.navigate_to_home()
            home_page.verify_home_page_loaded()
            expect(home_page.page).to_have_url(home_page.base_url + "/")
            home_page.take_screenshot("home_page")

        with allure.step("2. Переход на страницу логина"):
            login_page.navigate_to_login()
            login_page.verify_login_page_structure()
            expect(login_page.page).to_have_url(login_page.base_url + "/login")
            login_page.take_screenshot("login_page")

        with allure.step("3. Переход на админскую страницу (ожидаем редирект на логин)"):
            admin_page.navigate_to_admin()

            # После перехода на /admin ожидаем редирект на /login
            expect(admin_page.page).to_have_url(admin_page.base_url + "/login")

            # Проверяем что мы все еще на странице логина
            login_form = login_page.page.locator(login_page.login_form)
            expect(login_form).to_be_visible()

            admin_page.take_screenshot("admin_redirect_to_login")

            allure.attach(
                "Навигация завершена с учетом редиректов",
                name="Navigation",
                attachment_type=allure.attachment_type.TEXT
            )

    def test_direct_page_access(self, home_page, login_page, admin_page):
        """Тест прямого доступа к страницам с учетом защиты"""
        with allure.step("Прямой доступ к главной странице (должен работать)"):
            home_page.navigate_to_home()
            assert home_page.page.url == home_page.base_url + "/"
            allure.attach("Главная страница доступна напрямую", name="Home Access",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Прямой доступ к странице логина (должен работать)"):
            login_page.navigate_to_login()
            assert login_page.page.url == login_page.base_url + "/login"
            allure.attach("Страница логина доступна напрямую", name="Login Access",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Прямой доступ к админской странице (должен редиректить на логин)"):
            admin_page.navigate_to_admin()
            # Админская страница должна редиректить на логин
            assert admin_page.page.url == admin_page.base_url + "/login"
            allure.attach("Админская страница перенаправляет на логин", name="Admin Redirect",
                          attachment_type=allure.attachment_type.TEXT)

    def test_protected_routes_behavior(self, admin_page, login_page):
        """Тест поведения защищенных маршрутов"""
        with allure.step("Проверка защиты админской страницы"):
            admin_page.navigate_to_admin()

            with allure.step("Верификация редиректа на логин"):
                expect(admin_page.page).to_have_url(admin_page.base_url + "/login")

                # Проверяем что форма логина присутствует
                username_field = login_page.page.locator(login_page.username_input)
                password_field = login_page.page.locator(login_page.password_input)
                expect(username_field).to_be_visible()
                expect(password_field).to_be_visible()

                allure.attach(
                    "Защищенные маршруты корректно перенаправляют на аутентификацию",
                    name="Route Protection",
                    attachment_type=allure.attachment_type.TEXT
                )