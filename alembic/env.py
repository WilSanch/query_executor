import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Agregar ruta raíz para que Python encuentre 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import Base
from app.db.models.application import Application
from app.db.models.query_definition import QueryDefinition

# Carga configuración y logging
config = context.config
fileConfig(config.config_file_name)

# Si usas un archivo de settings con la URL de la DB, setéala aquí (opcional)
from app.core.config import settings
config.set_main_option('sqlalchemy.url', 'postgresql://admanausr:QQR78ab70e6b12021@psql-dnsdata-dev.postgres.database.azure.com:5432/query_executor')  # o como la tengas definida
print(settings.DATABASE_URL)

target_metadata = Base.metadata  # Esto es clave para autogenerar migraciones

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
