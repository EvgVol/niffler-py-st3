import json
from typing import Any

import allure

from playwright.sync_api import expect

from playwright.sync_api import Page, Locator

from niffler_ui_tests.support.logger import Logger
from niffler_ui_tests.support.utils import AllureAttachmentData

logger = Logger(name="root").logger


class Assertions:
    def __init__(
        self, *, page: Page, base_url: str, locator: Locator, element: str
    ):
        self.page = page
        self.base_url = base_url
        self.locator = locator
        self._element = element

    def _log_attach(self, action: str, details: Any = None) -> None:
        """Логирует и прикрепляет действие в Allure."""
        logger.info(
            "UI Assert | action=%s | element=%s | details=%s",
            action,
            self._element,
            json.dumps(details, ensure_ascii=False) if details else None,
        )

        with allure.step(f"UI Assert: {action}"):
            AllureAttachmentData(
                name="Element",
                body=self._element,
                attachment_type=allure.attachment_type.TEXT,
            ).attach()
            if details:
                AllureAttachmentData(
                    name="Details",
                    body=json.dumps(details, ensure_ascii=False, indent=2),
                    attachment_type=allure.attachment_type.JSON,
                ).attach()

    @allure.step("Проверить видимость элемента")
    def should_be_visible(self, timeout: int | None = 5):
        """Проверяет, что элемент виден."""
        self._log_attach(
            self.should_be_visible.__name__, details={"timeout": timeout}
        )
        expect(self.locator).to_be_visible(timeout=timeout * 10**3)

    @allure.step("Проверить возможность редактирования элемента")
    def should_be_editable(self, timeout: int | None = 5):
        """Проверяет, что элемент можно редактировать."""
        self._log_attach(
            self.should_be_editable.__name__, details={"timeout": timeout}
        )
        expect(self.locator).to_be_editable(timeout=timeout * 10**3)

    @allure.step("Проверить невидимость элемента")
    def should_be_not_visible(self, timeout: int | None = 5):
        """Проверяет, что элемент не видим."""
        self._log_attach(
            self.should_be_not_visible.__name__, details={"timeout": timeout}
        )
        expect(self.locator).not_to_be_visible(timeout=timeout * 10**3)

    @allure.step("Проверить наличие текста")
    def should_have_text(self, text: str, timeout: int | None = 5):
        """Проверяет, что элемент содержит указанный текст."""
        self._log_attach(
            self.should_have_text.__name__,
            details={"text": text, "timeout": timeout},
        )
        expect(self.locator).to_have_text(text, timeout=timeout * 10**3)
