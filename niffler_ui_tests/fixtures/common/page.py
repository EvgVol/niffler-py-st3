from typing import Generator, Any

import pytest

from playwright.sync_api import BrowserContext, Page
from niffler_ui_tests.support.reports import Report
from niffler_ui_tests.support.logger import Logger


@pytest.fixture(scope="session")
def page(browser_context: BrowserContext, request, logger) -> Generator[Page, Any, None]:
    """Фикстура для работы с отдельной страницей браузера."""
    page = browser_context.new_page()
    page.logger = logger
    logger.info("Создана новая страница браузера")
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    page.close()
    logger.info("=" * 40)
