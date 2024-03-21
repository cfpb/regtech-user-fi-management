import os
from pathlib import Path
from typing import Set
from urllib import parse

from pydantic import field_validator, PostgresDsn, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from regtech_api_commons.oauth2.config import KeycloakSettings


JWT_OPTS_PREFIX = "jwt_opts_"

env_files_to_load: list[Path | str] = [".env"]
if os.getenv("ENV", "LOCAL") == "LOCAL":
    env_files_to_load.append(".env.local")


class Settings(BaseSettings):
    inst_db_schema: str = "public"
    inst_db_name: str
    inst_db_user: str
    inst_db_pwd: str
    inst_db_host: str
    inst_db_scheme: str = "postgresql+asyncpg"
    inst_conn: str | None = None
    admin_scopes: Set[str] = set(["query-groups", "manage-users"])
    db_logging: bool = True

    def __init__(self, **data):
        super().__init__(**data)

    @field_validator("inst_conn", mode="before")
    @classmethod
    def build_postgres_dsn(cls, field_value, info: ValidationInfo) -> str:
        postgres_dsn = PostgresDsn.build(
            scheme=info.data.get("inst_db_scheme"),
            username=info.data.get("inst_db_user"),
            password=parse.quote(str(info.data.get("inst_db_pwd")), safe=""),
            host=info.data.get("inst_db_host"),
            path=info.data.get("inst_db_name"),
        )
        return postgres_dsn.unicode_string()

    model_config = SettingsConfigDict(env_file=env_files_to_load, extra="allow")


settings = Settings()

kc_settings = KeycloakSettings(_env_file=env_files_to_load)
