from niffler_ui_tests.src.database.db_response import DbResponse
from niffler_ui_tests.support._conditions.base_condition import Condition
from niffler_ui_tests.support.utils import AllureAttachmentData

from precisely import Matcher


class DbCondition(Condition):
    """
    Условие для проверки ответа из БД.
    """

    def __init__(
        self,
        response: DbResponse,
        matcher: Matcher,
        *,
        default_description: str,
        description: str = "",
        error_reason: str = "",
        expected_data_attachment: AllureAttachmentData | None = None,
    ):
        super().__init__(matcher, expected_data_attachment)
        self.response = response
        self.default_description = default_description
        self.description = description or default_description
        self.error_reason = error_reason

    def actual(self):
        """Фактическое значение для проверки."""
        return self.response.body

    def __str__(self):
        return (
            f"{self.description}\n"
            f"{super().__str__()}\n"
            f"SQL-запрос:\n{self.response.query}\n"
        )