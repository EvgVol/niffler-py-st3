import allure
import pytest

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


@pytest.mark.parametrize("field", ['поле ввода логина', 'поле ввода пароля'])
def test_editable_field(client: LoginPage, field: str):
    with allure.step("Открытие страницы авторизации"):
        login_page = client.open()
    with allure.step(f"Проверка возможности редактирования: {field}"):
        login_page.asserts(field).should_be_editable()
