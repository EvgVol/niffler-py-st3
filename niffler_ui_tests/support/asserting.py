from typing import Any

import allure
from precisely import assert_that, Matcher, equal_to

from niffler_ui_tests.support._conditions.base_condition import Condition
from niffler_ui_tests.support._conditions.value_condition import ValueCondition
from niffler_ui_tests.support.utils import AllureAttachmentData


class Assert:
    """
    Класс-обертка для ассертов.
    """

    @staticmethod
    def _attach_expected(condition: Condition) -> None:
        """
        Прикрепляет ожидаемые данные к Allure, если они есть.

        :param condition: Условие для проверки
        """
        condition.attach_expected()

    @classmethod
    def _should_have(cls, actual: Any, condition: Condition) -> None:
        cls._attach_expected(condition)
        try:
            assert_that(actual, condition.matcher)
        except AssertionError as e:
            msg = f"{getattr(condition, 'error_reason', '')}\n{str(e)}".strip()
            raise AssertionError(msg) from e

    @classmethod
    def equal(
        cls,
        value_to_check: Any,
        expected_value: Any,
        *,
        description: str = "",
        error_reason: str = "",
    ):
        """
        Проверяет, что значение равно ожидаемому.

        :param value_to_check: Фактическое значение.
        :param expected_value: Ожидаемое значение.
        :param description: Описание проверки.
        :param error_reason: Дополнительное пояснение при ошибке.
        :return:
        """
        cls._should_have(
            value_to_check,
            ValueCondition(
                matcher=equal_to(expected_value),
                default_description="Объект должен быть равен ожидаемому",
                description=description,
                error_reason=error_reason,
                expected_data_attachment=AllureAttachmentData(
                    name="Ожидаемый объект",
                    body=expected_value,
                    attachment_type=allure.attachment_type.JSON,
                ),
            ),
        )