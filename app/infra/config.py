import secrets
from typing import Any, List, Literal, Optional

from pydantic import AnyHttpUrl, BaseModel, BaseSettings, PostgresDsn, validator


class SNS_TOPIC(BaseModel):
    PROFILE_UPDATED: str


class SQS_QUEUE(BaseModel):
    USER_UPDATED: str
    KARMA_COIN_MINTED: str
    STUDENT_FUNDS_COURSES_UPDATED: str


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str
    ENV: Literal["local", "sandbox", "production"]

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None
    DB_ECHO_LOG: bool = False

    SNS: SNS_TOPIC
    SQS: SQS_QUEUE
    SNS_SQS_MAPPING: str = ""

    JWT_KEY_PASSWORD: str = "a1H4evK%E2O&"

    AWS_ACCOUNT_ID: str
    AWS_REGION: str
    AWS_ACCESS_KEY: str
    AWS_SNS_SQS_HOST: str = ""
    AWS_SECRET: str
    S3_MEDIA_BUCKET: str = "cq-development"
    SENTRY_DNS: str = ""

    # GetStream
    GETSTREAM_API_KEY: str
    GETSTREAM_SECRET: str

    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
        return dsn + "?prepared_statement_cache_size=0"

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"
        env_file = ".env"


settings = Settings()
