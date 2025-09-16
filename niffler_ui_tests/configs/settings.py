from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from niffler_ui_tests.configs.config import Config
from niffler_ui_tests.configs.loader.configs import load_config
from dotenv import load_dotenv


load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class BrowserSettings(BaseSettings):
    browser_name: Literal["chromium", "firefox", "webkit", "chrome"] = Field(
        default="chromium", alias="BROWSER_NAME"
    )
    executable_path: str | None = Field(default=None, alias="BROWSER_PATH")
    headless: bool = Field(default=False, alias="BROWSER_HEADLESS")
    width: int = Field(default=1280, alias="BROWSER_WIDTH")
    height: int = Field(default=720, alias="BROWSER_HEIGHT")
    record_video_dir: str = Field(
        default="reports/videos", alias="REPORT_PATH"
    )


class LoggingSettings(BaseSettings):
    enable: bool = Field(default=True, alias="LOG_ENABLE")
    level: str = Field(default="INFO", alias="LOG_LEVEL")
    dir: Path = Field(default=PROJECT_ROOT / "logs", alias="LOG_DIR")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        alias="LOG_FORMAT",
    )
    max_size: int = Field(default=5_000_000, alias="LOG_MAX_SIZE")  # 5 MB
    backup_count: int = Field(default=5, alias="LOG_BACKUP_COUNT")


class ReportSettings(BaseSettings):
    path: Path = Field(default=Path("reports"), alias="REPORT_PATH")


class Settings(BaseSettings):
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    report: ReportSettings = Field(default_factory=ReportSettings)
    config: Config | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__"
    )

    def load_config(self) -> "Settings":
        """Подгружает конфиг из YAML."""
        self.config = load_config(self.environment)
        return self


settings = Settings().load_config()
