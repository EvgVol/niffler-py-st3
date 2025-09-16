import logging

from playwright.sync_api import Locator


class Actions:
    """Класс с методами для взаимодействия с элементами страницы."""

    def __init__(self, element: Locator, logger: logging.Logger = None):
        self._element = element
        self.logger = logger

    @property
    def element(self) -> Locator:
        return self._element

    def __str__(self):
        """Возвращает удобочитаемое представление локатора."""
        try:
            return f"[{self._element.evaluate('el => el.outerHTML')[:100]}]"  # Обрезаем длинные селекторы
        except Exception:
            return "Не удалось определить селектор"

    def click(self):
        """Клик по элементу."""
        self.logger.info(f"Клик по элементу: {self}")
        self.element.click()

    def fill(self, text: str):
        """Заполняет поле ввода."""
        self.logger.info(f"Заполнение поля `{self}` значением: {text}")
        self.element.fill(text)

    def press(self, key: str):
        """Нажимает клавишу в поле ввода."""
        self.logger.info(f"Нажатие клавиши: {key}")
        self.element.press(key)

    def hover(self):
        """Наведение курсора на элемент."""
        self.logger.info(f"Наведение курсора на элемент: {self}")
        self.element.hover()
