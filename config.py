from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    mode: str = Field(alias="MODE")

    postgres_host: str = Field(alias="SQL_DB_HOST")
    postgres_port: int = Field(alias="SQL_DB_PORT")
    postgres_name: str = Field(alias="SQL_DB_NAME")
    postgres_user: str = Field(alias="SQL_DB_USER")
    postgres_pass: str = Field(alias="SQL_DB_PASS")

    smtp_user: str = Field(alias="SMTP_USER")
    smtp_password: str = Field(alias="SMTP_PASSWORD")

    smtp_host: str = Field(alias="SMTP_HOST")
    smtp_port: int = Field(alias="SMTP_PORT")

    redis_url: str = Field(alias="REDIS_URL")

    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def postgres_db_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pass}@{self.postgres_host}:" \
               f"{self.postgres_port}/{self.postgres_name}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
