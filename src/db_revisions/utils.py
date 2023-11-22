import os
import sys
from dotenv import load_dotenv
from alembic import op
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection

if getattr(sys, "frozen", False):
    # we are running in a bundle
    basedir = sys._MEIPast
else:
    # we are running in a normal Python environment
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(basedir)

# this specific to SBL configuration
env_file = os.path.join(basedir, ".env.local")

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


def table_exists(table_name):
    config = op.get_context().config
    engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.")
    inspector = reflection.Inspector.from_engine(engine)
    tables = inspector.get_table_names()
    return table_name in tables
