from pathlib import Path

import pytest
from niffler_ui_tests.support.reports import Report
from niffler_ui_tests.support.logger import Logger


@pytest.fixture(scope="session")
def logger(request, settings):
    """Фикстура для настройки логирования."""
    report = Report()
    log = Logger(
        name=request.node.name,
        log_dir=Path(settings.logging.dir)
    ).logger
    log.info(f"{"=" * 40}")
    log.info(f"Browser: {settings.browser.browser_name}")
    log.info(f"Viewport: {settings.browser.height} x {settings.browser.width}")
    log.info(f"Headless: {settings.browser.headless}")
    log.info(f"Report path: {settings.report.path}")
    log.info(f"{"-" * 40}")
    return log

@pytest.fixture(autouse=True)
def log_test_start_and_end(request, logger):
    """Логирование старта и окончания каждого теста."""
    logger.info(f"--- Тест {request.node.name} стартует ---")
    yield
    logger.info(f"--- Тест {request.node.name} завершен ---")
