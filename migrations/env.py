import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.infra.config import settings
from app.repository.db.schema.activity import Activity
from app.repository.db.schema.address import Address  # noqa: F401
from app.repository.db.schema.application import Application
from app.repository.db.schema.award import Award
from app.repository.db.schema.children_profile import ChildrenProfile
from app.repository.db.schema.college_universities import CollegeUniversities
from app.repository.db.schema.connection import ConnectionConnection
from app.repository.db.schema.connection_request import ConnectionRequestConnection
from app.repository.db.schema.education import Education  # noqa: F401
from app.repository.db.schema.grade import Grade
from app.repository.db.schema.profile import UserProfile  # noqa: F401
from app.repository.db.schema.profile_privacy import ProfilePrivacy
from app.repository.db.schema.roles import Roles
from app.repository.db.schema.score import Score
from app.repository.db.schema.student_fund_courses import StudentFundCourses
from app.repository.db.schema.test import Test
from app.repository.db.schema.user_karma import UserKarma
from app.repository.db.schema.voluntary import Voluntary
from app.repository.db.schema.work import Work
from app.shared.repository.db.schema.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

sqlalchemy_url = "postgresql+psycopg2://{user}:{password}@{host}/{db_name}".format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    db_name=settings.POSTGRES_DB,
)

config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
