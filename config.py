from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel


class DbSettings(BaseModel):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_SCHEMA: str = "postgresql+asyncpg"

    @property
    def url(self):
        url: str = PostgresDsn.build(scheme=self.DB_SCHEMA, host=self.DB_HOST, port=self.DB_PORT,
                                     username=self.DB_USER, password=self.DB_PASS,
                                     path=self.DB_NAME).unicode_string()

        return url


class BotSettings(BaseModel):
    basic_url: str = "http://158.160.138.75/api/v1/"
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__', env_file=".env")
    api_v1_prefix: str = "/api/v1"
    db: DbSettings
    bot: BotSettings
    rules_for_review: str = ("Это базовые критерии для ревью проектов. Они могут меняться от одного проекта к другому. "
                             "Вы можете воспользоваться ими, если нужно. Правила:\n\n"
                             "1. Код хорошо читается и понятно организован\n\n"
                             "2. Функциональность проекта соответствует задаче заказчика.\n\n"
                             "3. Код запускается и не выдает ошибку при попытке его запустить или как-либо "
                             "взаимодействовать с ним.\n\n"
                             "4. Присутствует документация к проекту.\n\n"
                             "5. Функции реализованы без багов и работают так, как описаны в документации к проекту.")


settings = Settings()
