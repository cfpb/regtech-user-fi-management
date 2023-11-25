import os
import sys
from typing import Dict, Any
from pydantic import TypeAdapter
from pydantic.networks import HttpUrl, PostgresDsn
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from alembic import command as alembic
from alembic.config import Config
from dotenv import load_dotenv


# Start Alembic
if getattr(sys, "frozen", False):
    # we are running in a bundle
    basedir = sys._MEIPast
else:
    # we are running in a normal Python environment
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(basedir)

alembic_dir = os.path.join(basedir, "db_revisions")
sys.path.append(alembic_dir)

# this specific to SBL configuration
env_file = os.path.join(basedir, "src/.env.local")

ENV = os.getenv("ENV", "LOCAL")

if ENV == "LOCAL":
    load_dotenv(env_file)
else:
    load_dotenv()

INST_DB_USER = os.environ.get("INST_DB_USER")
INST_DB_PWD = os.environ.get("INST_DB_PWD")
INST_DB_HOST = os.environ.get("INST_DB_HOST")
INST_DB_NAME = os.environ.get("INST_DB_NAME")
INST_DB_SCHEMA = os.environ.get("INST_DB_SCHEMA")
INST_DB_PATH = f"{INST_DB_USER}:{INST_DB_PWD}@{INST_DB_HOST}/{INST_DB_NAME}"
INST_DB_URL = f"postgresql://{INST_DB_USER}:{INST_DB_PWD}@{INST_DB_HOST}/{INST_DB_NAME}"
# end specific SBL configuration

def get_alembic_config(db_url: str = INST_DB_URL) -> Config:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", alembic_dir)
    alembic_cfg.set_main_option("sqlalchemy.url", str(db_url))
    return alembic_cfg


def upgrade_database(revision: str = "head", db_url: str = INST_DB_URL) -> None:
    alembic_cfg = get_alembic_config(db_url)
    alembic.upgrade(alembic_cfg, revision)

#End Alembic

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
