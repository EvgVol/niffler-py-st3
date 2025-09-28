import pytest

from niffler_ui_tests.configs.settings import Settings
from niffler_ui_tests.src.database.db_manager import DbManager


@pytest.fixture(scope="session")
def currency_niffler_db(settings: Settings) -> DbManager:
    db = DbManager(
        db_host=settings.config.app.currency_niffler.database.host,
        db_port=settings.config.app.currency_niffler.database.port,
        db_name=settings.config.app.currency_niffler.database.db_name,
        db_user=settings.environment.currency_niffler_db_user,
        db_password=settings.environment.currency_niffler_db_password,
    )
    with db as manager:
        yield manager
