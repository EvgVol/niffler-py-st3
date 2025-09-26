import pytest

from niffler_ui_tests.configs.settings import Settings
from niffler_ui_tests.src.database.db_manager import DbManager


@pytest.fixture(scope="session")
def auth_niffler_db(settings: Settings) -> DbManager:
    db = DbManager(
        db_host=settings.config.app.auth_niffler.database.host,
        db_port=settings.config.app.auth_niffler.database.port,
        db_name=settings.config.app.auth_niffler.database.db_name,
        db_user=settings.environment.auth_niffler_db_user,
        db_password=settings.environment.auth_niffler_db_password,
    )
    with db as manager:
        yield manager
