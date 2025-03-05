import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import AsyncIterator 
from sqlalchemy.exc import SQLAlchemyError

from app.infra.config import settings
from app.shared.utils.custom_json_serializer import _custom_json_serializer

logger = structlog.get_logger()

engine = create_async_engine(
    settings.DATABASE_URI,
    json_serializer=_custom_json_serializer,
    future=True,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "server_settings": {
            "application_name": (
                f"{settings.PROJECT_NAME.lower()}[{settings.ENV.lower()}]"
            )
        }
    },
)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


async def get_db() -> AsyncIterator[async_sessionmaker]:
    try:
        yield SessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)

