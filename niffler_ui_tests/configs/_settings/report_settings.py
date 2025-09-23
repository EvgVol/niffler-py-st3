from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings


class ReportSettings(BaseSettings):
    """
    Настройки генерации отчетов по результатам тестов.
    """

    path: Path = Field(
        default=Path("reports"), alias="REPORT_PATH",
        description="Путь до каталога отчетов"
    )
