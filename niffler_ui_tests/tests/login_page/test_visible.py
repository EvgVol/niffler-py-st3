import allure
import pytest

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


import allure
import pytest

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


@allure.epic("Аутентификация")
@allure.feature("Форма авторизации (Login)")
class TestLoginPageVisibility:
    """Тесты на проверку видимости элементов страницы логина."""

    @allure.story("Отображение логотипа")
    @allure.title("Логотип виден на странице")
    def test_visible_logo(self, client: LoginPage):
        with allure.step("Открытие страницы авторизации"):
            login_page = client.open()
        with allure.step("Проверка видимости логотипа"):
            login_page.asserts("логотип").should_be_visible()

    @allure.story("Отображение полей ввода")
    @allure.title("Поля авторизации видны на странице")
    @pytest.mark.parametrize(
        "field", ["поле ввода логина", "поле ввода пароля"],
        ids=['visible field login', 'visible field password'],
    )
    def test_visible_fields(self, client: LoginPage, field: str):
        with allure.step("Открытие страницы авторизации"):
            login_page = client.open()
        with allure.step(f"Проверка видимости: {field}"):
            login_page.asserts(field).should_be_visible()

    @allure.story("Отображение кнопок")
    @allure.title("Кнопки авторизации видны на странице")
    @pytest.mark.parametrize(
        "button", ["кнопка входа", "кнопка регистрации"],
        ids=['visible button login', 'visible button signup'],
    )
    def test_visible_buttons(self, client: LoginPage, button: str):
        with allure.step("Открытие страницы авторизации"):
            login_page = client.open()
        with allure.step(f"Проверка видимости: {button}"):
            login_page.asserts(button).should_be_visible()