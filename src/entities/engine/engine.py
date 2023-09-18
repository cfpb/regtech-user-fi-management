import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task

DB_URL = os.getenv("INST_CONN")
DB_SCHEMA = os.getenv("INST_DB_SCHEMA", "public")
engine = create_async_engine(DB_URL, echo=True).execution_options(schema_translate_map={None: DB_SCHEMA})
SessionLocal = async_scoped_session(async_sessionmaker(engine, expire_on_commit=False), current_task)


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
