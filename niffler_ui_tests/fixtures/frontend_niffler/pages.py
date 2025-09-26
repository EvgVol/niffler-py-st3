import pytest
from playwright.sync_api import Page

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage
from niffler_ui_tests.src.pages.main_page.main_page import MainPage


@pytest.fixture
def auth(settings, page: Page):
    login_page = LoginPage(
        base_url=settings.config.app.frontend_niffler.http, page=page
    )
    login_page.open()
    login_page.actions("поле ввода логина").fill("vol")
    login_page.actions("поле ввода пароля").fill("qwerty")
    login_page.actions("кнопка входа").click()
    return page


@pytest.fixture
def main_page(auth: Page) -> MainPage:
    """После авторизации возвращает объект MainPage."""
    return MainPage(base_url=auth.url, page=auth)


@pytest.fixture
def login_page(settings, page: Page) -> LoginPage:
    login_page = LoginPage(
        base_url=settings.config.app.frontend_niffler.http, page=page
    )
    login_page.open()
    return login_page
