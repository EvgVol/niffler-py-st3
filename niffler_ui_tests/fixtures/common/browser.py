import pytest

from niffler_ui_tests.src.playwright.browser_manager import BrowserManager
from playwright.sync_api import BrowserContext


@pytest.fixture
def browser_manager():
    """Фикстура для управления браузером."""
    with BrowserManager() as manager:
        yield manager


@pytest.fixture
def browser_context(browser_manager: BrowserManager) -> BrowserContext:
    """Фикстура для создания контекста браузера."""
    context_options = browser_manager.config.get_context_options()
    context = browser_manager.get_browser().new_context(**context_options)
    yield context
    context.close()
