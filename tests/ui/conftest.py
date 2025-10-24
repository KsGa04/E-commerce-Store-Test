import pytest
import sys
import os
from playwright.sync_api import sync_playwright, Page
import allure

# Добавляем корень проекта в Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

BASE_URL = "https://v0-swagger-backend-frontend.vercel.app"


@pytest.fixture(scope="session")
def browser():
    """Фикстура для запуска браузера"""
    with sync_playwright() as p:
        # Можно переключить на headless=True для CI/CD
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Фикстура для создания контекста браузера"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context) -> Page:
    """Фикстура для создания новой страницы"""
    page = context.new_page()
    page.set_default_timeout(15000) # 10 секунд таймаут по умолчанию

    # Прикрепляем информацию о странице к Allure
    allure.attach(
        f"Browser: Chromium\nViewport: 1920x1080\nTimeout: 10s",
        name="Browser Configuration",
        attachment_type=allure.attachment_type.TEXT
    )

    yield page
    page.close()


@pytest.fixture(scope="function")
def home_page(page: Page):
    """Фикстура для главной страницы"""
    from tests.ui.pages.home_page import HomePage
    return HomePage(page)


@pytest.fixture(scope="function")
def login_page(page: Page):
    """Фикстура для страницы логина"""
    from tests.ui.pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture(scope="function")
def admin_page(page: Page):
    """Фикстура для админской страницы"""
    from tests.ui.pages.admin_page import AdminPage
    return AdminPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для прикрепления скриншотов к Allure отчетам при падении тестов"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Получаем объект page из фикстуры
        page = None
        for fixturename in item.fixturenames:
            if fixturename == "page":
                page = item.funcargs[fixturename]
                break

        if page:
            # Делаем скриншот и прикрепляем к отчету
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )

            # Прикрепляем HTML контент страницы
            html_content = page.content()
            allure.attach(
                html_content,
                name="page_html_on_failure",
                attachment_type=allure.attachment_type.HTML
            )