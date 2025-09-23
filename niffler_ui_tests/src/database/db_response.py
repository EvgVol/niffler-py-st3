import json

from datetime import datetime
from typing import Any

import allure

from psycopg2.extras import RealDictRow


def _json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


class DbResponse:
    """Класс-обёртка для данных, полученных из БД."""

    def __init__(
        self,
        query: str,
        result: Any,
        rowcount: int | None = None,
        execution_time: float | None = None,
    ):
        """
        :param query: SQL-запрос.
        :param result: Результат запроса.
        :param rowcount: Количество строк в результате.
        :param execution_time: Время выполнения запроса в секундах.
        """
        self.query = query
        self.result = self._normalize_result(result)
        self.rowcount = (
            rowcount
            if rowcount is not None
            else (
                len(result)
                if isinstance(result, list)
                else (1 if result else 0)
            )
        )
        self.execution_time = execution_time
        self.timestamp = datetime.now().isoformat()

        self._attach_to_allure()

    @property
    def body(self):
        """Алиас для result."""
        return self.result

    def __str__(self):
        return (
            "\n====================== SQL QUERY ======================\n"
            f"{self.query}"
            "\n====================== SQL RESULT =====================\n"
            f"{json.dumps(self.result, ensure_ascii=False, indent=2, default=_json_serializer)}"
            "\n=======================================================\n"
            f"Затронуто строк: {self.rowcount}\n"
            f"Время выполнения: {self.execution_time or 'не замерено'} сек\n"
            f"Метка времени: {self.timestamp}\n"
            "=======================================================\n"
        )

    @staticmethod
    def _normalize_result(result: Any):
        """Привести RealDictRow к обычному dict."""
        if isinstance(result, RealDictRow):
            return dict(result)
        if isinstance(result, list) and all(
            isinstance(r, RealDictRow) for r in result
        ):
            return [dict(r) for r in result]
        return result

    def __len__(self):
        if isinstance(self.result, list):
            return len(self.result)
        return self.rowcount

    def __getitem__(self, item):
        if isinstance(self.result, list):
            return self.result[item]
        raise TypeError(
            "DbResponse не поддерживает индексацию, если result не список."
        )

    def _attach_to_allure(self):
        """Прикрепить SQL-запрос и результат к Allure-отчёту."""
        with allure.step("SQL-запрос к БД"):
            allure.attach(
                self.query,
                name="SQL-запрос",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                json.dumps(
                    self.result,
                    ensure_ascii=False,
                    indent=2,
                    default=_json_serializer,
                ),
                name="Результат SQL-запроса",
                attachment_type=allure.attachment_type.JSON,
            )
