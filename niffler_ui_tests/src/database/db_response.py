import json
import logging

from datetime import datetime
from typing import Any

import allure

from psycopg2.extras import RealDictRow

from niffler_ui_tests.support.logger import Logger
from niffler_ui_tests.support.utils import AllureAttachmentData, _json_serializer

logger = Logger(name="root").logger


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

        self._log_response()

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

    def _log_response(self):
        """Логировать и прикреплять SQL-запрос и результат."""
        logger.info(
            "SQL Response | query=%s | rowcount=%s | elapsed=%s | result=%s",
            self.query,
            self.rowcount,
            f"{self.execution_time:.4f}s" if self.execution_time else None,
            json.dumps(self.result, ensure_ascii=False, default=_json_serializer),
        )

        with allure.step("SQL-запрос и ответ БД"):
            AllureAttachmentData(
                name="SQL-запрос",
                body=self.query,
                attachment_type=allure.attachment_type.TEXT,
            ).attach()

            AllureAttachmentData(
                name="Результат SQL-запроса",
                body=self.result,
                attachment_type=allure.attachment_type.JSON,
            ).attach()