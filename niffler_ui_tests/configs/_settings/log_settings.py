from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class LoggingSettings(BaseSettings):
    """
    Настройки логирования для тестового фреймворка.

    Управляет форматом, уровнем логов и ротацией файлов логов.
    """

    enable: bool = Field(
        default=True, alias="LOG_ENABLE",
        description="Включить/выключить логирование")
    level: str = Field(
        default="INFO", alias="LOG_LEVEL",
        description="Уровень логирования"
    )
    dir: Path = Field(
        default=PROJECT_ROOT / "logs", alias="LOG_DIR",
        description="Путь до директории логов"
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        alias="LOG_FORMAT",
        description="Формат строки лога"
    )
    max_size: int = Field(
        default=5_000_000, alias="LOG_MAX_SIZE",
        description="Максимальный размер файла лога (в байтах)"
    )
    backup_count: int = Field(
        default=5, alias="LOG_BACKUP_COUNT",
        description="Количество резервных файлов логов"
    )