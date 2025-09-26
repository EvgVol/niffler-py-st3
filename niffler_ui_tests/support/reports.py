import datetime
import shutil
from pathlib import Path

from playwright.sync_api import Page, BrowserContext

from niffler_ui_tests.configs import settings


class Report:
    """Класс для работы с отчетом."""

    @property
    def report_path(self) -> Path:
        parent_root = Path(__file__).resolve().parents[2]
        return parent_root / Path(settings.report.path)

    def get_path(self, item, root_dir: Path, ext: str) -> Path:
        """Формирует путь для файла теста (скриншот/видео)."""
        now = datetime.datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%H-%M-%S")

        # item — это pytest.Function
        test_file = Path(str(item.fspath)).stem
        test_name = item.name

        test_dir = root_dir / date_folder / test_file / test_name
        test_dir.mkdir(parents=True, exist_ok=True)

        return test_dir / f"{test_file}_{test_name}_{timestamp}.{ext}"

    def save_screenshot(self, page: Page, item) -> None:
        screenshot_path = self.get_path(item, self.report_path, "png")
        page.screenshot(path=screenshot_path, full_page=True)

    def save_video(self, context: BrowserContext, item) -> None:
        video_path = self.get_path(item, self.report_path, "webm")
        last_page = context.pages[-1]

        if last_page.video and last_page.video.path():
            last_video_path = last_page.video.path()
            if Path(last_video_path).exists():
                shutil.copy(last_video_path, video_path)
