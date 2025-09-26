import pytest

from playwright.sync_api import Page
from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


@pytest.fixture(scope="session")
def client(settings, page: Page):
    return LoginPage(
        base_url=settings.config.app.frontend_niffler.http, page=page
    )
