from alembic import op
from sqlalchemy import engine_from_config
import sqlalchemy


def table_exists(table_name):
    config = op.get_context().config
    engine = config.attributes.get("connection", None)
    if engine is None:
        engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.")
    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    return table_name in tables
