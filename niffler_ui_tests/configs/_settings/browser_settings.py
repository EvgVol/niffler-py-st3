from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings


class BrowserSettings(BaseSettings):
    """
    Настройки браузера для запуска UI-тестов.

    Поддерживаются браузеры: chromium, firefox, webkit, chrome.
    Параметры читаются из переменных окружения.
    """

    browser_name: Literal["chromium", "firefox", "webkit", "chrome"] = Field(
        default="chromium", alias="BROWSER_NAME"
    )
    executable_path: str | None = Field(
        default=None,
        alias="BROWSER_PATH",
        description="Путь до бинарника браузера (если не указан, используется системный)",
    )
    headless: bool = Field(
        default=False,
        alias="BROWSER_HEADLESS",
        description="Запуск браузера в headless-режиме",
    )
    width: int = Field(
        default=1280, alias="BROWSER_WIDTH", description="Ширина окна браузера"
    )
    height: int = Field(
        default=720, alias="BROWSER_HEIGHT", description="Высота окна браузера"
    )
    record_video_dir: str = Field(
        default="reports/videos",
        alias="REPORT_PATH",
        description="Каталог для сохранения видео тестов",
    )
