import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from app.domain.student.data.award import RecognitionType, GradeType
from sqlalchemy.orm import mapped_column


class Award(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    title = mapped_column(sq.String(255), nullable=True)
    recognition_type = mapped_column(sq.Enum(RecognitionType))
    description = mapped_column(sq.String(1024), nullable=True)
    grade = mapped_column(sq.Enum(GradeType), nullable=True)