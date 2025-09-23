from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from niffler_ui_tests.configs._settings.browser_settings import BrowserSettings
from niffler_ui_tests.configs._settings.env_settings import EnvironmentSettings
from niffler_ui_tests.configs._settings.log_settings import LoggingSettings
from niffler_ui_tests.configs._settings.report_settings import ReportSettings
from niffler_ui_tests.configs.config import Config
from niffler_ui_tests.configs.loader.configs import load_config
from dotenv import load_dotenv


load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Глобальные настройки тестового фреймворка.

    Объединяет все секции настроек (окружение, браузер, логи, отчеты).
    """

    environment: EnvironmentSettings = Field(
        default_factory=EnvironmentSettings
    )
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    report: ReportSettings = Field(default_factory=ReportSettings)
    config: Config | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__"
    )

    def load_config(self) -> "Settings":
        """Подгружает конфиг из YAML."""
        self.config = load_config(self.environment.environment)
        return self


settings = Settings().load_config()
