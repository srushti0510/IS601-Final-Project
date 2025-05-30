from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Import your models and Base
from app.models.user_model import Base, User  # Explicit imports are crucial

# Debug output to verify model registration
print("!!! DEBUG: Tables in metadata:", Base.metadata.tables.keys())

# This is the Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        echo=True,  # This will show all SQL commands being executed
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine which mode to use
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()