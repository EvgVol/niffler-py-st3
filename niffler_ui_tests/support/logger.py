import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

from niffler_ui_tests.configs import settings


class Logger:
    """Класс для создания и настройки логгера."""

    def __init__(
        self,
        name: str,
        log_level: str = settings.logging.level,
        log_dir: Path = settings.logging.dir,
        max_file_size: int = settings.logging.max_size,
        backup_count: int = settings.logging.backup_count,
    ):
        """
        Инициализирует логгер с указанными параметрами.

        :param name: Имя логгера.
        :param log_level: Уровень логирования (например, "DEBUG", "INFO").
        :param log_dir: Директория для хранения файлов логов.
        :param max_file_size: Максимальный размер файла логов (в байтах).
        :param backup_count: Количество резервных файлов.
        """
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"

        formatter = logging.Formatter(settings.logging.format)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(
            getattr(logging, log_level.upper(), logging.INFO)
        )
        self._logger.handlers.clear()
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count
        )
        file_handler.setFormatter(formatter)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        if not settings.logging.enable:
            self._logger.disabled = True

    @property
    def log_path(self) -> Path:
        """Возвращает путь к директории логов."""
        return settings.logging.dir

    @property
    def logger(self) -> logging.Logger:
        """Возвращает экземпляр логгера."""
        return self._logger
