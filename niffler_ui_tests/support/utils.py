import re
from typing import Any

import allure

from precisely import Matcher
from precisely.results import matched, unmatched


class AllureAttachmentData:
    """
    Данные для прикрепления в Allure.
    """

    def __init__(
        self, name: str, body: Any, attachment_type=allure.attachment_type.JSON
    ):
        """
        :param name: Название прикрепляемого объекта
        :param body: Объект для прикрепления
        :param attachment_type: Тип прикрепляемого объекта (по умолчанию JSON)
        """
        self.name = name
        self.body = body
        self.attachment_type = attachment_type


class RegexMatcher:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, value):
        if isinstance(value, str) and self.pattern.match(value):
            return matched()
        return unmatched(
            f"'{value}' does not match regex '{self.pattern.pattern}'"
        )

    def describe(self):
        return f"string matching regex '{self.pattern.pattern}'"


class PasswordHashMatcher(Matcher):
    HASH_PREFIXES = {
        "bcrypt": r"^\{bcrypt\}\$2[aby]?\$\d{2}\$[./A-Za-z0-9]{53}$",
        "sha256": r"^\{sha256\}[A-Fa-f0-9]{64}$",
        "argon2": r"^\{argon2\}\$argon2(id|i|d)\$v=\d+\$.*",
    }

    def __init__(self, hash_type: str):
        self.hash_type = hash_type
        self.regex = re.compile(self.HASH_PREFIXES[hash_type])

    def match(self, value):
        if isinstance(value, str) and self.regex.match(value):
            return matched()
        return unmatched(f"'{value}' is not a valid {self.hash_type} hash")

    def describe(self):
        return f"password hashed with {self.hash_type}"
