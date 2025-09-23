from enum import StrEnum

from pydantic import BaseModel


class DbType(StrEnum):
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    SQLITE = "SQLite"


DB_TYPES = {
    DbType.POSTGRESQL: "postgresql+psycopg2",
    DbType.MYSQL: "mysql+pymysql",
    DbType.SQLITE: "sqlite+pysqlite",
}


class DbConfig(BaseModel):
    """Конфигурация подключения к БД."""

    host: str
    port: int
    db_name: str
    db_user: str
    db_password: str
    db_type: DbType = DbType.POSTGRESQL

    def build_url(self) -> str:
        """Формирует URL для подключения к БД."""
        driver = DB_TYPES[self.db_type]
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.host}:{self.port}/{self.db_name}"
