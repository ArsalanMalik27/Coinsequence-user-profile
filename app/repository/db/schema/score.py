import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Score(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    subject_name = mapped_column(sq.String(255))
    score = mapped_column(sq.String(200))
    date = mapped_column(sq.Date, nullable=True)
    activated_at = mapped_column(sq.DateTime, nullable=True)
    subject_id = mapped_column(UUID(as_uuid=True))
    test_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("test.id", ondelete="CASCADE")
    )
