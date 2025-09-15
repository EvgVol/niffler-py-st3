import pytest
from niffler_ui_tests.configs.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings().load_config()
