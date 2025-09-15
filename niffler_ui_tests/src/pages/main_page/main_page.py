from playwright.sync_api import Page
from niffler_ui_tests.src.playwright.base_page import BasePage
from niffler_ui_tests.src.pages.main_page.main_locators import MainPageLocators


class MainPage(BasePage):

    def __init__(self, page: Page, **kwargs):
        super().__init__(locators_class=MainPageLocators, **kwargs)
        self.page = page
