from typing import Literal

from playwright.sync_api import Locator as PlaywrightLocator
from playwright.sync_api import Page
from pydantic import BaseModel, model_validator


class Locator(BaseModel):
    """Класс для работы с локаторами.

    Используется для унификации работы с локаторами в Playwright,
    позволяя указывать метод поиска элемента и его значение.

    :param name: Имя локатора.
    :param selector: CSS / XPATH селектор.
    :param method: Метод поиска элемента:
        - "role": поиск по ARIA-ролям (button, textbox, link, etc.).
        - "text": поиск по тексту.
        - "label": поиск по label.
        - "placeholder": поиск по placeholder.
        - "alt_text": поиск по alt_text.
        - "title": поиск по title.
        - "test_id": поиск по test_id.
    :param value: Значение для поиска.
    :param kwargs: Дополнительные параметры для методов, например, "name" для "role".

    Примеры:
    locator = Locator(name="Поле ввода", method="placeholder", value="Введите имя")
    locator = Locator(name="Поле ввода", selector="input[type=text]")
    locator = Locator(name="Поле ввода", method="text", value="Введите имя")
    """

    name: str
    selector: str | None = None
    method: (
        Literal[
            "role",
            "text",
            "label",
            "placeholder",
            "alt_text",
            "title",
            "test_id",
        ]
        | None
    ) = None
    value: str | None = None
    kwargs: dict | None = None

    @model_validator(mode="after")
    def check_locator(self):
        """Валидация: должен быть указан либо selector, либо method + value."""
        errors = []

        if self.method and not self.value:
            errors.append(f"Для метода '{self.method}' необходимо указать 'value'.")

        if not self.method and not self.selector:
            errors.append("Необходимо указать либо 'selector', либо 'method' + 'value'.")

        if errors:
            raise ValueError(" ".join(errors))

        return self

    def get_locator(self, page: Page, **kwargs) -> PlaywrightLocator:
        """Возвращает Playwright-локатор в зависимости от метода."""
        if self.method:
            method_map = {
                "role": page.get_by_role,
                "text": page.get_by_text,
                "label": page.get_by_label,
                "placeholder": page.get_by_placeholder,
                "alt_text": page.get_by_alt_text,
                "title": page.get_by_title,
                "test_id": page.get_by_test_id,
            }
            if self.method == "role":
                return method_map[self.method](self.value, **(self.kwargs or {}), **kwargs)
            return method_map[self.method](self.value, **kwargs)
        return page.locator(self.selector)

    def __str__(self) -> str:
        """Строковое представление локатора."""
        if self.method:
            if self.method == "role" and self.kwargs:
                return f"{self.name}: get_by_{self.method}('{self.value}', {self.kwargs})"
            return f"{self.name}: get_by_{self.method}('{self.value}')"
        return f"{self.name}: {self.selector}"
