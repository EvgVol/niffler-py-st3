from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    """
    Настройки окружения для запуска тестов.

    Содержит информацию о среде (dev/stage/prod) и доступах к базе данных.
    """

    model_config = SettingsConfigDict(env_prefix="")

    environment: str = Field(
        default="dev", alias="ENVIRONMENT",
        description="Текущее окружение"
    )
    auth_niffler_db_user: str = Field(
        alias="AUTH_NIFFLER_DB_USER",
        description="Пользователь БД niffler-auth"
    )
    auth_niffler_db_password: str = Field(
        alias="AUTH_NIFFLER_DB_PASSWORD",
        description="Пароль БД niffler-auth"
    )
    currency_niffler_db_user: str = Field(
        alias="CURRENCY_NIFFLER_DB_USER",
        description="Пользователь БД niffler-currency"
    )
    currency_niffler_db_password: str = Field(
        alias="CURRENCY_NIFFLER_DB_PASSWORD",
        description="Пароль БД niffler-currency"
    )
    spend_niffler_db_user: str = Field(
        alias="SPEND_NIFFLER_DB_USER",
        description="Пользователь БД niffler-spend"
    )
    spend_niffler_db_password: str = Field(
        alias="SPEND_NIFFLER_DB_PASSWORD",
        description="Пароль БД niffler-spend"
    )
    userdata_niffler_db_user: str = Field(
        alias="USERDATA_NIFFLER_DB_USER",
        description="Пользователь БД niffler-userdata"
    )
    userdata_niffler_db_password: str = Field(
        alias="USERDATA_NIFFLER_DB_PASSWORD",
        description="Пароль БД niffler-userdata"
    )