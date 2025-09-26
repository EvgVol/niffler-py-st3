import json
import re
import allure
from typing import TypeAlias, Any

from playwright.sync_api import expect, Page, Locator as PlaywrightLocator

from niffler_ui_tests.src.playwright.actions import Actions
from niffler_ui_tests.src.playwright.assertions import Assertions
from niffler_ui_tests.src.playwright.locator import Locator
from niffler_ui_tests.support.logger import Logger
from niffler_ui_tests.support.utils import AllureAttachmentData

ElementName: TypeAlias = str
LocatorType: TypeAlias = PlaywrightLocator | ElementName

logger = Logger(name="root").logger


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

    def _log_attach(
        self, action: str, element: Any = None, details: Any = None
    ) -> None:
        """Логирует и прикрепляет действие в Allure."""

        element_str = str(element) if element is not None else "N/A"
        details_str = (
            json.dumps(details, ensure_ascii=False, indent=2)
            if details
            else None
        )

        logger.info(
            "UI Action | action=%s | element=%s | details=%s",
            action,
            element_str,
            details_str,
        )

        with allure.step(f"UI Action: {action}"):
            AllureAttachmentData(
                name="Element",
                body=element_str,
                attachment_type=allure.attachment_type.TEXT,
            ).attach()

            if details:
                AllureAttachmentData(
                    name="Details",
                    body=details_str,
                    attachment_type=allure.attachment_type.JSON,
                ).attach()

    @allure.step("Переход по URL: {url}")
    def go_to(self, url: str):
        self._log_attach("Перейти по URL", element=url)
        self.page.goto(url)

    @allure.step("Открытие базовой страницы")
    def open(self):
        self._log_attach("Открыть базовую страницу", element=self.base_url)
        self.page.goto(f"{self.base_url}")
        return self

    @allure.step("Переключение на новую вкладку")
    def switch_to_new_tab(self) -> "BasePage":
        """Переключается на новую вкладку и возвращает объект BasePage."""
        new_tab = self.page.context.wait_for_event("page")
        new_tab.wait_for_load_state()
        self._log_attach("Переключиться на новую вкладку", element=new_tab.url)
        return new_tab

    def actions(self, name: LocatorType) -> Actions:
        return Actions(locator=self.element(name), element=name)

    def asserts(self, name: LocatorType) -> Assertions:
        """Возвращает объект с ассершенами для страницы."""
        return Assertions(
            page=self.page,
            base_url=self.base_url,
            locator=self.element(name),
            element=name,
        )

    @allure.step("Проверка, что URL содержит: {url_part}")
    def should_contain_url(self, url_part: str, timeout: int | None = None):
        """
        Проверяет, что текущий URL содержит указанный фрагмент.
        """
        self._log_attach(
            "Проверка URL",
            element=self.page.url,
            details={"contains": url_part},
        )
        expect(self.page).to_have_url(
            re.compile(f".*{url_part}.*"), timeout=timeout or 5000
        )

    @allure.step("Пауза с таймаутом {timeout} секунд")
    def pause(self, timeout: float):
        self._log_attach(
            "Пауза", element="wait_for_timeout", details={"timeout": timeout}
        )
        self.page.wait_for_timeout(timeout * 10**3)
