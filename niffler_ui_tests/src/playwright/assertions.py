import allure
import logging

from playwright.sync_api import expect

from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class Assertions:
    def __init__(self, *, page: Page, base_url: str, element: Locator):
        self.page = page
        self.base_url = base_url
        self.element = element

    @allure.step("Проверить видимость элемента")
    def should_be_visible(self, timeout: int | None = 5):
        """Проверяет, что элемент виден."""
        logger.info("Проверяем, что элемент виден")
        expect(self.element).to_be_visible(timeout=timeout * 10**3)
        logger.debug(f"Элемент виден: {self.element}")

    @allure.step("Проверить возможность редактирования элемента")
    def should_be_editable(self, timeout: int | None = 5):
        """Проверяет, что элемент можно редактировать."""
        expect(self.element).to_be_editable(timeout=timeout * 10**3)

    @allure.step("Проверить невидимость элемента")
    def should_be_not_visible(self, timeout: int | None = 5):
        """Проверяет, что элемент не видим."""
        expect(self.element).not_to_be_visible(timeout=timeout * 10**3)

    @allure.step("Проверить наличие текста")
    def should_have_text(self, text: str, timeout: int | None = 5):
        """Проверяет, что элемент содержит указанный текст."""
        expect(self.element).to_have_text(text, timeout=timeout * 10**3)
