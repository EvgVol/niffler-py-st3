import re
from pathlib import Path

import pytest
from niffler_ui_tests.support.logger import Logger


@pytest.fixture
def logger(request, settings) -> Logger:
    """Логгер на каждый тест."""
    safe_name = re.sub(r"[:/\\]", "_", request.node.nodeid)
    log = Logger(
        name=safe_name,
        log_dir=Path(settings.logging.dir),
        log_level=settings.logging.level,
    ).logger

    log.info("=" * 70)
    log.info(f"START TEST: {request.node.nodeid}")
    log.info(
        f"Browser: {settings.browser.browser_name} | "
        f"Viewport: {settings.browser.height}x{settings.browser.width} | "
        f"Headless: {settings.browser.headless}"
    )
    log.info("-" * 70)
    yield log
    log.info(f"END TEST: {request.node.nodeid}")
    log.info("=" * 70)


@pytest.fixture(autouse=True)
def log_test_start_and_end(request, settings, logger):
    """Логирование старта и окончания каждого теста."""
    test_name = request.node.name
    browser = settings.browser.browser_name
    viewport = f"{settings.browser.height}x{settings.browser.width}"
    headless = settings.browser.headless

    logger.info(
        f"START {test_name} | {browser} {viewport} headless={headless}"
    )
    yield
    logger.info(f"END   {test_name} | SUCCESS")
