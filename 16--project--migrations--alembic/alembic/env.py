import asyncio
from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

# Import all ORM models before creating tables
import app.models.orm  # noqa: F401
# Note:
# Alembic uses the same asynchronous database driver and connection URL as the application.
# Although migrations could be executed through a separate synchronous driver,
# sharing a single configuration keeps the setup consistent and avoids configuration drift.
from app.repositories.sqlalchemy.database import async_engine, DATABASE_URL


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # Note:
    # Alembic exposes synchronous migration APIs
    # such as `context.configure()` and `context.run_migration()`.
    # `AsyncConnection.run_sync()` bridges the gap by providing a synchronous `Connection`
    # on top of the asynchronous database driver, allowing Alembic to run migrations
    # without requiring a separate synchronous engine.

    async with async_engine.begin() as connection:
        # Configure Alembic using a synchronous `Connection`
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata,
            )
        )

        # Execute all pending migrations
        await connection.run_sync(
            lambda conn: context.run_migrations()
        )


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
