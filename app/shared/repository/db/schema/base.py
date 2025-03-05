import uuid

import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()


class BaseTableMixin(object):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # type: ignore
    created_at = mapped_column(sq.DateTime)
    updated_at = mapped_column(sq.DateTime)
    deleted = mapped_column(sq.Boolean, default=False)

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
