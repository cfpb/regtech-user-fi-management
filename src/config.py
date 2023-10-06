import os
from pydantic import TypeAdapter

from pydantic_settings import BaseSettings, SettingsConfigDict

JWT_OPTS_PREFIX = "jwt_opts_"

env_files_to_load = [".env"]
if os.getenv("ENV", "LOCAL") == "LOCAL":
    env_files_to_load.append(".env.local")


class Settings(BaseSettings):
    inst_conn: str = ""
    inst_db_schema: str = "public"
    auth_client: str = ""
    auth_url: str = ""
    token_url: str = ""
    certs_url: str = ""
    kc_url: str = ""
    kc_realm: str = ""
    kc_admin_client_id: str = ""
    kc_admin_client_secret: str = ""
    kc_realm_url: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        jwt_opts_adapter = TypeAdapter(int | bool)
        self.jwt_opts = {
            key.replace(JWT_OPTS_PREFIX, ""): jwt_opts_adapter.validate_python(value)
            for (key, value) in self.model_extra.items()
            if key.startswith(JWT_OPTS_PREFIX)
        }

    model_config = SettingsConfigDict(env_file=env_files_to_load, extra="allow")


try:
    settings = Settings()
except Exception as e:
    raise SystemExit(f"failed to set up settings [{e}]")
