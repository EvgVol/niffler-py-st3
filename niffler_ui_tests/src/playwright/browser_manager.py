from typing import Literal, TypeAlias, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Playwright
from pydantic import Field
from pydantic_settings import BaseSettings


BrowserName: TypeAlias = Literal["chromium", "firefox", "webkit", "chrome"]


class BrowserConfig(BaseSettings):
    """Конфигурация браузера из переменных окружения."""

    browser_name: BrowserName = Field(default="chromium", alias="BROWSER_NAME")
    executable_path: str | None = Field(default=None, alias="BROWSER_PATH")
    headless: bool = Field(default=False, alias="BROWSER_HEADLESS")
    width: int = Field(default=1280, alias="BROWSER_WIDTH")
    height: int = Field(default=720, alias="BROWSER_HEIGHT")
    record_video_dir: str = Field(default="reports/videos", alias="REPORT_PATH")

    def get_launch_options(self) -> dict[str, Any]:
        """Параметры запуска браузера."""
        options = {"headless": self.headless}
        if self.browser_name in ["chromium", "chrome"] and self.executable_path:
            options["executable_path"] = self.executable_path
        return options

    def get_context_options(self) -> dict[str, Any]:
        """Параметры создания контекста браузера."""
        return {
            "viewport": {"width": self.width, "height": self.height},
            "record_video_dir": self.record_video_dir,
        }


class BrowserManager:
    """Управляет запуском браузеров через Playwright."""

    def __init__(self):
        self.config = BrowserConfig()
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None

    def __enter__(self):
        """Запускает Playwright."""
        self.playwright = sync_playwright().start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Закрывает браузер и Playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_browser(self) -> Browser:
        """Создаёт новый экземпляр браузера."""
        if not self.playwright:
            raise RuntimeError(
                "Playwright не запущен. Используйте 'with BrowserManager()'."
            )
        browser_name = self.config.browser_name
        if browser_name == "chrome": browser_name = "chromium"
        browser_type = getattr(self.playwright, browser_name)
        self.browser = browser_type.launch(**self.config.get_launch_options())
        return self.browser

    def get_context(self) -> BrowserContext:
        """Создаёт новый контекст браузера с опциями."""
        if not self.browser:
            self.browser = self.get_browser()
        return self.browser.new_context(**self.config.get_context_options())
