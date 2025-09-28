import pytest

from niffler_ui_tests.support.reports import Report


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Хук, чтобы в каждом тесте были доступны rep_setup/rep_call/rep_teardown."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed and "page" in item.fixturenames:
        page = item.funcargs["page"]
        report = Report()

        try:
            report.save_screenshot(page, item)
        except Exception as e:
            print(f"[Report] Ошибка сохранения скриншота: {e}")

        try:
            report.save_video(page.context, item)
        except Exception as e:
            print(f"[Report] Ошибка сохранения видео: {e}")


# @pytest.fixture(autouse=True)
# def cleanup_reports(settings):
#     """Удаляет папки reports и logs после завершения тестов."""
#     yield
#     reports_dir = Path(settings.report.path)
#     log_dir = Path(settings.logging.dir)
#
#     if reports_dir.exists():
#         shutil.rmtree(reports_dir)
#
#     if log_dir.exists():
#         shutil.rmtree(log_dir)
