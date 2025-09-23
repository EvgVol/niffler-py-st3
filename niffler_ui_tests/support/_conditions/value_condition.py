from niffler_ui_tests.support._conditions.base_condition import Condition
from niffler_ui_tests.support.utils import AllureAttachmentData
from precisely import Matcher


class ValueCondition(Condition):
    """
    Условие для проверки значения.
    """
    def __init__(
        self,
        matcher: Matcher,
        *,
        default_description: str,
        description: str = "",
        error_reason: str = "",
        expected_data_attachment: AllureAttachmentData | None = None,
    ):
        """
        :param matcher: Матчер для проверки
        :param default_description: Описание проверки по умолчанию.
        :param description: Пользовательское описание проверки.
        :param error_reason: Дополнительное пояснение при ошибке.
        :param expected_data_attachment: Данные для вложения в отчет Allure.
        """
        super().__init__(matcher, expected_data_attachment)
        self.default_description = default_description
        self.description = description or default_description
        self.error_reason = error_reason