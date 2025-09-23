import allure
from precisely import Matcher

from niffler_ui_tests.support.utils import AllureAttachmentData


class Condition:
    """
    Базовое условие для проверки.
    """
    def __init__(
            self, matcher: Matcher, expected_data_attachment: AllureAttachmentData | None = None
    ):
        """
        :param matcher: Матчер для проверки
        :param expected_data_attachment: Данные для вложения в отчет Allure.
        """
        self.matcher = matcher
        self.expected_data_attachment = expected_data_attachment

    def attach_expected(self):
        if self.expected_data_attachment:
            allure.attach(
                str(self.expected_data_attachment.body),
                name=self.expected_data_attachment.name,
                attachment_type=self.expected_data_attachment.attachment_type,
            )

    def describe(self) -> str:
        return str(self.matcher)