from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "private-messenger"
    environment: str = "dev"
    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: str = Field(..., alias="REDIS_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_ttl_seconds: int = 3600
    s3_endpoint: str | None = Field(default=None, alias="S3_ENDPOINT")
    s3_access_key: str | None = Field(default=None, alias="S3_ACCESS_KEY")
    s3_secret_key: str | None = Field(default=None, alias="S3_SECRET_KEY")
    s3_bucket: str | None = Field(default=None, alias="S3_BUCKET")
    turn_static_auth_secret: str | None = Field(default=None, alias="TURN_SECRET")
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"], alias="ALLOWED_ORIGINS")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


SettingsDep = Annotated[Settings, Depends(get_settings)]
