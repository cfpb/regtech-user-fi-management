import os
import logging
import re
from urllib import parse
from typing import Dict, Any

from pydantic import TypeAdapter, field_validator, FieldValidationInfo
from pydantic.networks import HttpUrl, PostgresDsn
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

JWT_OPTS_PREFIX = "jwt_opts_"

env_files_to_load = [".env"]
if os.getenv("ENV", "LOCAL") == "LOCAL":
    env_files_to_load.append(".env.local")


class Settings(BaseSettings):
    inst_conn: PostgresDsn
    inst_db_schema: str = "public"
    auth_client: str
    auth_url: HttpUrl
    token_url: HttpUrl
    certs_url: HttpUrl
    kc_url: HttpUrl
    kc_realm: str
    kc_admin_client_id: str
    kc_admin_client_secret: SecretStr
    kc_realm_url: HttpUrl
    jwt_opts: Dict[str, bool | int] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.set_jwt_opts()

    @field_validator("inst_conn", mode="before")
    @classmethod
    def encode_db_password(cls, postgres_dsn, info: FieldValidationInfo) -> Any:
        log = logging.getLogger()
        pwd = re.search(".*:.*:(.*)@", postgres_dsn)
        if pwd:
            pwd_str = pwd.group(1)
            encoded_password = parse.quote(pwd_str, safe="")
            return postgres_dsn.replace(pwd_str, encoded_password)
        else:
            log.error(f"Postgres DSN did not contain a properly formatted URL: {postgres_dsn}")

    def set_jwt_opts(self) -> None:
        """
        Converts `jwt_opts_` prefixed settings, and env vars into JWT options dictionary.
        all options are boolean, with exception of 'leeway' being int
        valid options can be found here:
        https://github.com/mpdavis/python-jose/blob/4b0701b46a8d00988afcc5168c2b3a1fd60d15d8/jose/jwt.py#L81

        Because we're using model_extra to load in jwt_opts as a dynamic dictionary,
        normal env overrides does not take place on top of dotenv files,
        so we're merging settings.model_extra with environment variables.
        """
        jwt_opts_adapter = TypeAdapter(int | bool)
        self.jwt_opts = {
            **self.parse_jwt_vars(jwt_opts_adapter, self.model_extra.items()),
            **self.parse_jwt_vars(jwt_opts_adapter, os.environ.items()),
        }

    def parse_jwt_vars(self, type_adapter: TypeAdapter, setting_variables: Dict[str, Any]) -> Dict[str, bool | int]:
        return {
            key.lower().replace(JWT_OPTS_PREFIX, ""): type_adapter.validate_python(value)
            for (key, value) in setting_variables
            if key.lower().startswith(JWT_OPTS_PREFIX)
        }

    model_config = SettingsConfigDict(env_file=env_files_to_load, extra="allow")


settings = Settings()
