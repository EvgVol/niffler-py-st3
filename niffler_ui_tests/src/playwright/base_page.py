import re
from typing import TypeAlias
import logging

from playwright.sync_api import expect, Page, Locator as PlaywrightLocator

from niffler_ui_tests.src.playwright.actions import Actions
from niffler_ui_tests.src.playwright.assertions import Assertions
from niffler_ui_tests.src.playwright.locator import Locator


ElementName: TypeAlias = str
LocatorType: TypeAlias = PlaywrightLocator | ElementName

logger = logging.getLogger(__name__)


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, base_url: str, page: Page, locators_class=None):
        self.base_url = base_url
        self.page = page
        self._locators_class = locators_class
        self._locators = BasePage._collect_locators(locators_class)

    @classmethod
    def _collect_locators(cls, locators_class):
        """Собирает локаторы из переданного класса."""
        return {
            loc.name: loc
            for loc in locators_class.__dict__.values()
            if isinstance(loc, Locator)
        }

    @property
    def locators(self):
        return self._locators

    def element(self, name: LocatorType) -> PlaywrightLocator:
        """Возвращает Playwright-локатор."""
        if isinstance(name, PlaywrightLocator):
            return name

        locator = self.locators.get(name)
        if not locator:
            msg = f"Локатор с именем '{name}' не найден"
            logger.error(msg)
            raise ValueError(msg)
        return locator.get_locator(self.page)

    def go_to(self, url: str):
        self.page.goto(url)
        logger.info(f"Открыта страница: {self.page.url}")

    def open(self):
        self.page.goto(f"{self.base_url}")
        logger.info(f"Открыта страница: {self.page.url}")
        return self

    def switch_to_new_tab(self) -> "BasePage":
        """Переключается на новую вкладку и возвращает объект BasePage."""
        new_tab = self.page.context.wait_for_event("page")
        new_tab.wait_for_load_state()
        logger.info(f"Открыта новая вкладка: {self.page.url}")
        return new_tab

    def actions(self, name: LocatorType) -> Actions:
        return Actions(self.element(name), logger)

    def asserts(self, name: LocatorType) -> Assertions:
        """Возвращает объект с ассершенами для страницы."""
        return Assertions(
            page=self.page, base_url=self.base_url, element=self.element(name)
        )

    def should_contain_url(self, url_part: str, timeout: int | None = None):
        """
        Проверяет, что текущий URL содержит указанный фрагмент.
        """
        expect(self.page).to_have_url(
            re.compile(f".*{url_part}.*"), timeout=timeout or 5000
        )
