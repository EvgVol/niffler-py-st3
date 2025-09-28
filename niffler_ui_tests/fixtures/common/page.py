from typing import Generator, Any

import pytest

from playwright.sync_api import BrowserContext, Page


@pytest.fixture
def page(
    browser_context: BrowserContext, request
) -> Generator[Page, Any, None]:
    """Фикстура для работы с отдельной страницей браузера."""
    record_video = request.node.get_closest_marker("record_video")
    if record_video:
        browser_context.tracing.start(screenshots=True, snapshots=True)
    page = browser_context.new_page()
    yield page
    page.close()
