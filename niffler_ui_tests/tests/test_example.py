import allure
from niffler_ui_tests.src.pages.login_page.login_page import LoginPage
from playwright.sync_api import expect



@allure.title("Логотип виден на странице")
def test_logo(client: LoginPage):
    with allure.step("Открытие страницы"):
        login_page = client.open()
    with allure.step("Проверка видимости логотипа"):
        login_page.asserts('логотип').should_be_visible()


