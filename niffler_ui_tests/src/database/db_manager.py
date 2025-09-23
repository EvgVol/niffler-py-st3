from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from niffler_ui_tests.src.database.db_client import DbClient
from niffler_ui_tests.src.database.db_config import DbConfig


class DbManager(DbClient):
    """
    Менеджер для работы с базами данных через SQLModel.
    """

    def __init__(
        self,
        db_name: str,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
        echo: bool = False,
        pool_size: int = 5,
    ) -> None:
        self.database_url = DbConfig(
            host=db_host,
            port=db_port,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
        )
        self.engine: Engine = create_engine(
            url=self.database_url.build_url(),
            connect_args={"connect_timeout": 3},
            echo=echo,
            pool_size=pool_size,
        )
        self._session: Session | None = None
        super().__init__(session=None)

    def open_session(self) -> Session:
        """Открывает сессию."""
        if self._session is None:
            self._session = Session(self.engine)
            self.session = self._session
        return self._session

    def close_session(self, exc_type=None, exc_val=None, exc_tb=None) -> None:
        """Закрывает сессию."""
        if self._session:
            if exc_type is None:
                self._session.commit()
            else:
                self._session.rollback()
            self._session.close()
            self._session = None

    def __enter__(self) -> DbClient:
        """Возвращает клиент для работы с SQL через контекст."""
        self.open_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Закрывает сессию через контекст."""
        self.close_session(exc_type, exc_val, exc_tb)
