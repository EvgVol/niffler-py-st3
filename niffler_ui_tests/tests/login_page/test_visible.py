import allure
import pytest

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


@allure.title("Логотип виден на странице")
def test_visible_logo(client: LoginPage):
    with allure.step("Открытие страницы авторизации"):
        login_page = client.open()
    with allure.step("Проверка видимости логотипа"):
        login_page.asserts("логотип").should_be_visible()

@allure.title("Поля авторизации видны на странице")
@pytest.mark.parametrize("field", ["поле ввода логина", "поле ввода пароля"])
def test_visible_fields(client: LoginPage, field: str):
    with allure.step("Открытие страницы авторизации"):
        login_page = client.open()
    with allure.step(f"Проверка видимости: {field}"):
        login_page.asserts(field).should_be_visible()


@allure.title("Кнопки авторизации видны на странице")
@pytest.mark.parametrize("button", ["кнопка входа", "кнопка регистрации"])
def test_visible_buttons(client: LoginPage, button: str):
    with allure.step("Открытие страницы авторизации"):
        login_page = client.open()
    with allure.step(f"Проверка видимости: {button}"):
        login_page.asserts(button).should_be_visible()
