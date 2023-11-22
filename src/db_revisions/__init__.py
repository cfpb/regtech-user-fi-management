import os
import logging
from alembic import command as alembic
from alembic.config import Config
from .utils import INST_DB_URL, basedir

log = logging.getLogger()


def get_alembic_config(db_url: str = INST_DB_URL) -> Config:
    alembic_dir = os.path.join(basedir, "db_revisions")
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", alembic_dir)
    alembic_cfg.set_main_option("sqlalchemy.url", str(db_url))
    return alembic_cfg


def upgrade_database(revision: str = "head", db_url: str = INST_DB_URL) -> None:
    alembic_cfg = get_alembic_config(db_url)
    alembic.upgrade(alembic_cfg, revision)
