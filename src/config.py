import os
from typing import Dict
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
    jwt_opts: Dict[str, bool | int] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.set_jw_opts()

    def set_jw_opts(self) -> None:
        """
        Converts `jwt_opts_` prefixed settings into JWT options dictionary.
        all options are boolean, with exception of 'leeway' being int
        valid options can be found here:
        https://github.com/mpdavis/python-jose/blob/4b0701b46a8d00988afcc5168c2b3a1fd60d15d8/jose/jwt.py#L81
        """
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
