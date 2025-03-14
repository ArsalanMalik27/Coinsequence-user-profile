import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from app.domain.student.data.roles import ParticipationTimeType
from app.domain.student.data.award import GradeType
from sqlalchemy.orm import mapped_column


class Roles(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    title = mapped_column(sq.String(255), nullable=True)
    description = mapped_column(sq.String(1024), nullable=True)
    participation_time_type = mapped_column(sq.Enum(ParticipationTimeType))
    hours_spent = mapped_column(sq.String(255), nullable=True)
    grade=mapped_column(sq.Enum(GradeType), nullable=True)
    start_date = mapped_column(sq.DateTime, nullable=True)
    end_date = mapped_column(sq.DateTime, nullable=True)