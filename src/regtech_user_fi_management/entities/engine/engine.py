from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from regtech_user_fi_management.config import settings

engine = create_engine(str(settings.inst_conn), echo=settings.db_logging).execution_options(
    schema_translate_map={None: settings.inst_db_schema}
)
SessionLocal = Session = sessionmaker(engine, expire_on_commit=False)


def get_session():
    with Session() as session:
        yield session
