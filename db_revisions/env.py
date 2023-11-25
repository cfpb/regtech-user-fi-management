from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context
from entities.models import Base
from config import INST_DB_URL, INST_DB_SCHEMA

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", INST_DB_URL)
# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata
target_metadata.schema = INST_DB_SCHEMA

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """configuration = config.get_section(config.config_ini_section)

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, version_table_schema=target_metadata.schema
        )
        with context.begin_transaction():
            context.run_migrations()"""

    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = engine_from_config(
            context.config.get_section(context.config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata, version_table_schema=target_metadata.schema
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
