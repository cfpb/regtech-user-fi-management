from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from regtech_user_fi_management.config import settings

engine = create_engine(str(settings.inst_conn), echo=settings.db_logging).execution_options(
    schema_translate_map={None: settings.inst_db_schema}
)
SessionLocal = scoped_session(sessionmaker(engine, expire_on_commit=False))


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
