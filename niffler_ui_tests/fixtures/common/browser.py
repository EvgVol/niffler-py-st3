import pytest

from niffler_ui_tests.src.playwright.browser_manager import BrowserManager
from playwright.sync_api import BrowserContext


@pytest.fixture(scope="session")
def browser_manager():
    """Фикстура для управления браузером."""
    with BrowserManager() as manager:
        yield manager


@pytest.fixture(scope="session")
def browser_context(browser_manager: BrowserManager, request, settings) -> BrowserContext:
    """Фикстура для создания контекста браузера."""
    record_video = request.node.get_closest_marker("record_video")

    context_options = browser_manager.config.get_context_options()

    if record_video:
        context_options["record_video_dir"] = settings.report.path

    context = browser_manager.get_browser().new_context(**context_options)
    yield context
    context.close()