import allure
from typing import Any

from precisely import equal_to, not_, includes, mapping_includes

from niffler_ui_tests.src.database.db_response import DbResponse
from niffler_ui_tests.support._conditions.database_condition import DbCondition
from niffler_ui_tests.support.asserting import Assert
from niffler_ui_tests.support.utils import (
    AllureAttachmentData,
    PasswordHashMatcher,
)


class AssertDB(Assert):
    """
    Проверки, специфичные для DbResponse.
    """

    @staticmethod
    def _build_matcher(
        expected_item: Any,
        field_name: str | None = None,
        hash_type: str | None = None,
    ):
        """
        Возвращает matcher для проверки значения в БД.
        Если expected_item — dict, использует mapping_includes.
        Если hash_type указан, возвращает PasswordHashMatcher для поля password.
        """
        if hash_type and field_name == "password":
            return includes(
                mapping_includes({field_name: PasswordHashMatcher(hash_type)})
            )
        if isinstance(expected_item, dict):
            return includes(mapping_includes(expected_item))
        return includes(expected_item)

    @classmethod
    def db_equal(
        cls,
        response: DbResponse,
        expected_value: Any,
        *,
        description: str = "",
        error_reason: str = "",
    ):
        """Проверяет, что результат SQL-запроса равен ожидаемому значению."""
        condition = DbCondition(
            response=response,
            matcher=equal_to(expected_value),
            default_description="Значение в БД должно быть равно ожидаемому",
            description=description,
            error_reason=error_reason,
            expected_data_attachment=AllureAttachmentData(
                name="Ожидаемое значение из БД",
                body=expected_value,
                attachment_type=allure.attachment_type.JSON,
            ),
        )
        cls._should_have(response.body, condition)

    @classmethod
    def db_not_null(
        cls,
        response: DbResponse,
        *,
        description: str = "",
        error_reason: str = "",
    ):
        """Проверяет, что результат SQL-запроса не NULL."""
        condition = DbCondition(
            response=response,
            matcher=not_(equal_to(None)),
            default_description="Значение в БД не должно быть NULL",
            description=description,
            error_reason=error_reason,
        )
        cls._should_have(response.body, condition)

    @classmethod
    def db_contains(
        cls,
        response: DbResponse,
        expected_item: Any,
        *,
        description: str = "",
        error_reason: str = "",
    ):
        """
        Проверяет, что результат SQL-запроса содержит ожидаемый элемент.

        :param response: Ответ от БД.
        :param expected_item: Ожидаемый элемент.
        :param description: Описание проверки.
        :param error_reason: Причина ошибки.
        """
        matcher = cls._build_matcher(expected_item)
        condition = DbCondition(
            response=response,
            matcher=matcher,
            default_description="Результат запроса должен содержать ожидаемый элемент",
            description=description,
            error_reason=error_reason,
            expected_data_attachment=AllureAttachmentData(
                name="Ожидаемый элемент",
                body=expected_item,
                attachment_type=allure.attachment_type.JSON,
            ),
        )
        cls._should_have(response.body, condition)

    @classmethod
    def db_password_hashed(
        cls,
        response: DbResponse,
        field_name: str = "password",
        hash_type: str | None = None,
        *,
        description: str = "",
        error_reason: str = "",
    ):
        """
        Проверяет, что поле `password` содержит хэшированный пароль.

        :param response: DbResponse с результатом SQL-запроса
        :param field_name: имя поля для проверки (по умолчанию "password")
        :param hash_type: ожидаемый тип хэширования (например: "bcrypt", "argon2", "pbkdf2").
                          Если None → проверяются все поддерживаемые.
        :param description: Описание проверки
        :param error_reason: Причина ошибки
        """

        supported_types = ("bcrypt", "argon2", "pbkdf2")
        if hash_type and hash_type not in supported_types:
            raise ValueError(
                f"hash_type должен быть одним из {supported_types}, но получен: {hash_type}"
            )

        expected_body = (
            f"{{{hash_type}}}..."
            if hash_type
            else "{" + "|".join(supported_types) + "}..."
        )
        matcher = cls._build_matcher(
            {}, field_name=field_name, hash_type=hash_type
        )

        condition = DbCondition(
            response=response,
            matcher=matcher,
            default_description=f"Поле `{field_name}` должно содержать хэшированный пароль",
            description=description,
            error_reason=error_reason,
            expected_data_attachment=AllureAttachmentData(
                name="Ожидаемый формат пароля",
                body=expected_body,
                attachment_type=allure.attachment_type.TEXT,
            ),
        )
        cls._should_have(response.body, condition)
