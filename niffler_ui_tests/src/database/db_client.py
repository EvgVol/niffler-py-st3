import logging
import time
from typing import Any

import allure
from sqlalchemy import text
from sqlmodel import Session

from niffler_ui_tests.src.database.db_response import DbResponse

logger = logging.getLogger(__name__)


class DbClient:
    """Клиент для работы с SQL-запросами через SQLModel."""

    def __init__(self, session: Session, schema: str = "public"):
        self.session = session
        self._table: str | None = None
        self._schema: str = schema

    @property
    def full_table(self) -> str:
        """Полное имя таблицы schema.table"""
        if not self._table:
            raise ValueError(
                "Таблица не выбрана. Используй .use_table(table)."
            )
        return f"{self._schema}.{self._table}"

    def use_table(self, table: str, schema: str | None = None) -> "DbClient":
        """
        Установить таблицу (и при необходимости схему).

        :param table: Имя таблицы
        :param schema: имя схемы (по умолчанию "public")
        """
        self._table = table
        if schema:
            self._schema = schema
        return self

    @staticmethod
    def _log_query(query: str, elapsed: float, params: dict | None = None):
        msg = f"SQL executed in {elapsed:.4f}s: {query}"
        if params:
            msg += f" | params: {params}"
        logger.info(msg)
        allure.attach(
            msg, name="SQL Log", attachment_type=allure.attachment_type.TEXT
        )

    def execute_query(
        self, query: str, params: dict | None = None
    ) -> DbResponse:
        """
        Выполнить INSERT/UPDATE/DELETE/DDL.

        :param query: SQL-запрос
        :param params: параметры для подстановки
        :return: DbResponse с числом затронутых строк
        """
        start = time.perf_counter()
        self.session.exec(text(query), params=params or {})
        self.session.commit()
        elapsed = round(time.perf_counter() - start, 4)
        self._log_query(query, elapsed, params)
        return DbResponse(query, None, rowcount=-1, execution_time=elapsed)

    def fetch_one(self, query: str, params: dict | None = None) -> DbResponse:
        """
        Выполнить SELECT и вернуть одну строку.

        :param query: SQL-запрос
        :param params: параметры для подстановки
        :return: DbResponse с одной записью
        """
        start = time.perf_counter()
        statement = text(query)
        if params:
            statement = statement.params(**params)
        result = self.session.exec(statement).mappings().first()
        elapsed = round(time.perf_counter() - start, 4)
        self._log_query(query, elapsed, params)
        return DbResponse(
            query,
            dict(result) if result else None,
            rowcount=1 if result else 0,
            execution_time=elapsed,
        )

    def fetch_all(self, query: str, params: dict | None = None) -> DbResponse:
        """
        Выполнить SELECT и вернуть все строки.

        :param query: SQL-запрос
        :param params: параметры для подстановки
        :return: DbResponse со списком записей
        """
        start = time.perf_counter()
        statement = text(query)
        if params:
            statement = statement.params(**params)
        results = self.session.exec(statement).mappings().all()
        elapsed = round(time.perf_counter() - start, 4)
        self._log_query(query, elapsed, params)
        return DbResponse(
            query,
            [dict(r) for r in results],
            rowcount=len(results),
            execution_time=elapsed,
        )

    def scalar(self, query: str, params: dict | None = None) -> DbResponse:
        """
        Выполнить SELECT и вернуть одно скалярное значение.

        :param query: SQL-запрос
        :param params: параметры для подстановки
        :return: DbResponse с одиночным значением
        """
        resp = self.fetch_one(query, params)
        if resp.body:
            resp.result = list(resp.body.values())[0]
        return resp

    def exists(self, query: str, params: dict | None = None) -> DbResponse:
        """
        Проверить, есть ли хотя бы одна строка по запросу.

        :param query: SQL-запрос
        :param params: параметры для подстановки
        :return: DbResponse с результатом True/False
        """
        resp = self.fetch_one(query, params)
        resp.result = bool(resp.body)
        return resp

    def filter_by(
        self,
        conditions: dict[str, Any],
        limit: int | None = None,
        order_by: str | None = None,
        desc: bool = True,
    ) -> DbResponse:
        where_clauses = []
        for k, v in conditions.items():
            if v is None:
                where_clauses.append(f"{k} IS NULL")
            elif isinstance(v, (list, tuple, set)):
                in_values = ", ".join(repr(x) for x in v)
                where_clauses.append(f"{k} IN ({in_values})")
            elif isinstance(v, str) and v.startswith((">=", "<=", ">", "<")):
                where_clauses.append(f"{k} {v}")
            else:
                where_clauses.append(f"{k} = {repr(v)}")

        query = f"SELECT * FROM {self.full_table}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if order_by:
            query += f" ORDER BY {order_by} {'DESC' if desc else 'ASC'}"
        if limit:
            query += f" LIMIT {limit}"

        with allure.step(
            f"Фильтрация записей таблицы {self.full_table} по условиям {conditions}"
        ):
            result = self.fetch_all(query)
            self._log_query(query, result.execution_time)
            return result

    def count(self, conditions: dict[str, Any] | None = None) -> int:
        """
        Посчитать количество записей с фильтром.

        :param conditions: Словарь вида {field: value} для WHERE
        """
        query = f"SELECT COUNT(*) AS cnt FROM {self.full_table}"
        if conditions:
            where_clauses = []
            for k, v in conditions.items():
                if v is None:
                    where_clauses.append(f"{k} IS NULL")
                else:
                    where_clauses.append(f"{k} = {repr(v)}")
            query += " WHERE " + " AND ".join(where_clauses)

        with allure.step(
            f"Подсчёт количества записей в таблице {self._table} с условиями {conditions}"
        ):
            resp = self.fetch_one(query)
            self._log_query(query, resp.execution_time)
            return resp.body["cnt"] if resp and resp.body else 0

    def delete(self, conditions: dict[str, Any]) -> DbResponse:
        """
        Удалить записи по условиям.

        :param conditions: Словарь вида {field: value} для WHERE
        :return: DbResponse
        """
        where_clauses = []
        for k, v in conditions.items():
            if v is None:
                where_clauses.append(f"{k} IS NULL")
            else:
                where_clauses.append(f"{k} = {repr(v)}")

        where_sql = " AND ".join(where_clauses)
        query = f"DELETE FROM {self.full_table} WHERE {where_sql}"

        with allure.step(
            f"Удаление записей из {self.full_table} по условиям {conditions}"
        ):
            result = self.execute_query(query)
            self._log_query(query, result.execution_time)
            return result
