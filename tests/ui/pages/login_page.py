from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Класс для работы со страницей логина"""

    def __init__(self, page: Page):
        super().__init__(page)
        # Локаторы
        self.card_title = '[data-slot="card-title"]'
        self.card_description = '[data-slot="card-description"]'
        self.username_input = '#username'
        self.password_input = '#password'
        self.login_button = '[data-slot="button"]'
        self.credentials_hint = "text=Default credentials: admin / admin123"
        self.login_form = 'form'

    def navigate_to_login(self):
        """Переход на страницу логина"""
        with allure.step("Переход на страницу логина"):
            self.navigate("/login")
            self.page.wait_for_load_state("networkidle")

    def verify_login_page_structure(self):
        """Проверка структуры страницы логина"""
        with allure.step("Проверка структуры страницы логина"):
            # Проверка заголовка
            expect(self.page).to_have_title("v0 App")

            # Проверка элементов карточки
            card_title = self.page.locator(self.card_title)
            expect(card_title).to_have_text("Login")

            card_description = self.page.locator(self.card_description)
            expect(card_description).to_have_text("Enter your credentials to access the admin panel")

            allure.attach(
                "Login page structure verified successfully",
                name="Page Structure",
                attachment_type=allure.attachment_type.TEXT
            )

    def verify_form_elements(self):
        """Проверка элементов формы"""
        with allure.step("Проверка элементов формы логина"):
            # Поле username
            username_input = self.page.locator(self.username_input)
            expect(username_input).to_be_visible()
            expect(username_input).to_have_attribute("placeholder", "admin")
            expect(username_input).to_have_attribute("type", "text")
            expect(username_input).to_have_attribute("required", "")

            # Поле password
            password_input = self.page.locator(self.password_input)
            expect(password_input).to_be_visible()
            expect(password_input).to_have_attribute("placeholder", "admin123")
            expect(password_input).to_have_attribute("type", "password")
            expect(password_input).to_have_attribute("required", "")

            # Кнопка логина
            login_button = self.page.locator(self.login_button)
            expect(login_button).to_have_text("Login")
            expect(login_button).to_have_attribute("type", "submit")

            # Подсказка с credentials
            credentials_hint = self.page.locator(self.credentials_hint)
            expect(credentials_hint).to_be_visible()

            allure.attach(
                "All form elements verified successfully",
                name="Form Elements",
                attachment_type=allure.attachment_type.TEXT
            )

    def login(self, username: str, password: str):
        """Выполнение логина"""
        with allure.step(f"Выполнение логина с пользователем: {username}"):
            # Очищаем поля и заполняем их
            username_field = self.page.locator(self.username_input)
            password_field = self.page.locator(self.password_input)

            username_field.fill("")
            username_field.fill(username)
            password_field.fill("")
            password_field.fill(password)

            # Прикрепляем информацию о введенных данных (без пароля)
            allure.attach(
                f"Username: {username}\nPassword: {'*' * len(password)}",
                name="Login Credentials",
                attachment_type=allure.attachment_type.TEXT
            )

            # Кликаем на кнопку логина
            login_button = self.page.locator(self.login_button)
            login_button.click()

            # Ждем возможного редиректа или изменений
            self.page.wait_for_timeout(3000)

            # Делаем скриншот после попытки логина
            self.take_screenshot("after_login_attempt")

    def login_with_valid_credentials(self):
        """Логин с валидными credentials"""
        from tests.ui.utills.helpers import Helpers
        test_data = Helpers.get_test_data()
        credentials = test_data["valid_credentials"]
        self.login(credentials["username"], credentials["password"])

    def login_with_invalid_credentials(self):
        """Логин с невалидными credentials"""
        from tests.ui.utills.helpers import Helpers
        test_data = Helpers.get_test_data()
        credentials = test_data["invalid_credentials"]
        self.login(credentials["username"], credentials["password"])

    def is_login_successful(self) -> bool:
        """Проверка успешности логина - улучшенная версия"""
        with allure.step("Проверка успешности логина"):
            try:
                # Ждем изменения URL или появления элементов админки
                self.page.wait_for_timeout(2000)
                current_url = self.page.url

                # Прикрепляем текущий URL для отладки
                allure.attach(
                    f"Current URL: {current_url}",
                    name="URL After Login",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Проверяем несколько условий успешного логина:
                # 1. Ушли со страницы логина
                if "/login" in current_url:
                    allure.attach("Still on login page", name="Login Status",
                                  attachment_type=allure.attachment_type.TEXT)
                    return False

                # 2. Проверяем, есть ли элементы админской панели
                loading_elements = self.page.locator("text=Loading...")
                admin_elements = self.page.locator("text=Admin")

                # Если видим loading или admin элементы, считаем логин успешным
                if loading_elements.count() > 0 or admin_elements.count() > 0:
                    allure.attach("Admin elements detected", name="Login Status",
                                  attachment_type=allure.attachment_type.TEXT)
                    return True

                # 3. Проверяем, что форма логина исчезла
                login_form = self.page.locator(self.login_form)
                if not login_form.is_visible():
                    allure.attach("Login form disappeared", name="Login Status",
                                  attachment_type=allure.attachment_type.TEXT)
                    return True

                # 4. Дополнительная проверка - если URL изменился на /admin
                if "/admin" in current_url:
                    allure.attach("Redirected to admin page", name="Login Status",
                                  attachment_type=allure.attachment_type.TEXT)
                    return True

                allure.attach("No success criteria met", name="Login Status",
                              attachment_type=allure.attachment_type.TEXT)
                return False

            except Exception as e:
                allure.attach(f"Error checking login success: {e}", name="Login Error",
                              attachment_type=allure.attachment_type.TEXT)
                return False

    def is_login_failed(self) -> bool:
        """Проверка неудачного логина"""
        with allure.step("Проверка неудачного логина"):
            try:
                self.page.wait_for_timeout(2000)
                current_url = self.page.url

                # Если остались на странице логина и форма видима
                if "/login" in current_url:
                    login_form = self.page.locator(self.login_form)
                    is_visible = login_form.is_visible()

                    allure.attach(
                        f"On login page: True\nLogin form visible: {is_visible}",
                        name="Login Failure Check",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    return is_visible

                allure.attach("Not on login page", name="Login Failure Check",
                              attachment_type=allure.attachment_type.TEXT)
                return False
            except Exception as e:
                allure.attach(f"Error checking login failure: {e}", name="Login Error",
                              attachment_type=allure.attachment_type.TEXT)
                return False

    def get_error_message(self) -> str:
        """Получение сообщения об ошибке, если есть"""
        with allure.step("Поиск сообщений об ошибках"):
            try:
                # Ищем возможные элементы с сообщениями об ошибках
                error_selectors = [
                    '[role="alert"]',
                    '.error',
                    '.alert',
                    'text=/error/i',
                    'text=/invalid/i',
                    'text=/incorrect/i'
                ]

                for selector in error_selectors:
                    elements = self.page.locator(selector)
                    if elements.count() > 0:
                        error_text = elements.first.inner_text()
                        allure.attach(f"Error found: {error_text}", name="Error Message",
                                      attachment_type=allure.attachment_type.TEXT)
                        return error_text

                allure.attach("No error message found", name="Error Message",
                              attachment_type=allure.attachment_type.TEXT)
                return "No error message found"
            except:
                allure.attach("Error retrieving message", name="Error Message",
                              attachment_type=allure.attachment_type.TEXT)
                return "Error retrieving message"