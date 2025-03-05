import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from app.domain.student.data.work import WorkType
from sqlalchemy.orm import mapped_column


class Work(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    title = mapped_column(sq.String(255), nullable=True)
    description = mapped_column(sq.String(1024), nullable=True)
    work_type = mapped_column(sq.Enum(WorkType))
    net_hours = mapped_column(sq.String(255), nullable=True)
    start_date = mapped_column(sq.DateTime, nullable=True)
    end_date = mapped_column(sq.DateTime, nullable=True)