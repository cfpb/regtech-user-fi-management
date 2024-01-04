from typing import Any, List, Dict
from alembic import op
from sqlalchemy import MetaData, Table, engine_from_config
import sqlalchemy


def table_exists(table_name):
    config = op.get_context().config
    engine = config.attributes.get("connection", None)
    if engine is None:
        engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.")
    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    return table_name in tables


def get_table_by_name(table_name):
    meta = MetaData()
    meta.reflect(op.get_bind())
    table = Table(table_name, meta)
    return table


def get_indices_from_collection(data: List[Dict[Any, Any]], key: str) -> List[Any]:
    return [e[key] for e in data]
