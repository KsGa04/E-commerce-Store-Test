import pytest
from playwright.sync_api import expect
import allure

@pytest.mark.ui
@pytest.mark.smoke
class TestHomePage:
    """Тесты для главной страницы"""

    def test_home_page_loading(self, home_page):
        """Тест загрузки главной страницы"""
        with allure.step("Переход на главную страницу"):
            home_page.navigate_to_home()

        with allure.step("Проверка загрузки главной страницы"):
            # Увеличиваем таймаут для стабильности
            home_page.page.wait_for_load_state("networkidle", timeout=15000)
            home_page.verify_home_page_loaded()

        with allure.step("Проверка доступности главной страницы"):
            home_page.verify_home_page_accessible()

    def test_home_page_meta_tags(self, home_page):
        """Тест мета-тегов главной страницы"""
        home_page.navigate_to_home()
        home_page.page.wait_for_load_state("networkidle", timeout=15000)

        with allure.step("Проверка мета-тегов"):
            meta_generator = home_page.page.locator('meta[name="generator"]')
            expect(meta_generator).to_have_attribute("content", "v0.app")

            meta_viewport = home_page.page.locator('meta[name="viewport"]')
            expect(meta_viewport).to_have_attribute("content", "width=device-width, initial-scale=1")

            allure.attach("Мета-теги проверены успешно", name="Meta Tags", attachment_type=allure.attachment_type.TEXT)

    def test_home_page_structure(self, home_page):
        """Тест структуры главной страницы"""
        home_page.navigate_to_home()
        home_page.page.wait_for_load_state("networkidle", timeout=15000)

        with allure.step("Проверка структуры страницы"):
            expect(home_page.page.locator("body")).to_be_visible(timeout=10000)
            expect(home_page.page.locator("html")).to_have_attribute("lang", "en")

            body = home_page.page.locator("body")
            expect(body).to_have_class("font-sans antialiased")

            allure.attach("Структура страницы проверена успешно", name="Page Structure",
                          attachment_type=allure.attachment_type.TEXT)

    def test_home_page_content(self, home_page):
        """Тест контента главной страницы"""
        home_page.navigate_to_home()
        home_page.page.wait_for_load_state("networkidle", timeout=15000)

        with allure.step("Проверка основного контента"):
            expect(home_page.page).to_have_title("v0 App")

            body_content = home_page.page.locator("body").text_content()
            assert body_content is not None, "Страница должна содержать контент"
            assert len(body_content) > 0, "Контент страницы не должен быть пустым"

            home_page.take_screenshot("home_page_content")

            allure.attach(
                f"Контент страницы проверен (длина: {len(body_content)} символов)",
                name="Page Content",
                attachment_type=allure.attachment_type.TEXT
            )

    def test_home_page_no_redirect(self, home_page):
        """Тест что главная страница доступна без редиректа"""
        home_page.navigate_to_home()
        home_page.page.wait_for_load_state("networkidle", timeout=15000)

        with allure.step("Проверка отсутствия редиректа"):
            expect(home_page.page).to_have_url(home_page.base_url + "/")
            assert "/login" not in home_page.page.url, "Главная страница не должна перенаправлять на логин"

            allure.attach(
                "Главная страница доступна без редиректа",
                name="No Redirect",
                attachment_type=allure.attachment_type.TEXT
            )