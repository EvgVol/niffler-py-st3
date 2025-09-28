import json
from typing import Any

import allure

from playwright.sync_api import Locator

from niffler_ui_tests.support.logger import Logger
from niffler_ui_tests.support.utils import AllureAttachmentData

logger = Logger(name="root").logger


class Actions:
    """Класс с методами для взаимодействия с элементами страницы."""

    def __init__(self, locator: Locator, element: str):
        self._locator = locator
        self._element = element

    @property
    def locator(self) -> Locator:
        return self._locator

    def __str__(self):
        """Возвращает удобочитаемое представление локатора."""
        try:
            return f"[{self._locator.evaluate('el => el.outerHTML')[:100]}]"  # Обрезаем длинные селекторы
        except Exception:
            return "Не удалось определить селектор"

    def _log_attach(self, action: str, details: Any = None) -> None:
        """Логирует и прикрепляет действие в Allure."""
        logger.info(
            "UI Action | action=%s | element=%s | details=%s",
            action,
            self._element,
            json.dumps(details, ensure_ascii=False) if details else None,
        )

        with allure.step(f"UI Action: {action}"):
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

    def click(self):
        """Клик по элементу."""
        self._log_attach(self.click.__doc__)
        self._locator.click()

    def fill(self, text: str):
        """Заполняет поле ввода."""
        self._log_attach(self.fill.__doc__, {"value": text})
        self._locator.fill(text)

    def press(self, key: str):
        """Нажимает клавишу в поле ввода."""
        self._log_attach(self.press.__doc__, {"key": key})
        self._locator.press(key)

    def hover(self):
        """Наведение курсора на элемент."""
        self._log_attach(
            self.hover.__doc__,
        )
        self._locator.hover()
