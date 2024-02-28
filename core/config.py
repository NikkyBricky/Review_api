from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "sqlite3.db"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    rules_for_review: str = ("Это базовые критерии для ревью проектов. Они могут меняться от одного проекта к другому."
                             "Вы можете воспользоваться ими, если нужно. Правила:\n\n"
                             "1. Код хорошо читается и понятно организован\n\n"
                             "2. Функциональность проекта соответствует задаче заказчика.\n\n"
                             "3. Код запускается и не выдает ошибку при попытке его запустить или как-либо"
                             "взаимодействовать с ним.\n\n"
                             "4. Присутствует документация к проекту.\n\n"
                             "5. Функции реализованы без багов и работают так, как описаны в документации к проекту.")


settings = Settings()
