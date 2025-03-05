import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.shared.repository.db.schema.base import Base, BaseTableMixin


class CollegeUniversities(Base, BaseTableMixin):
    profile_id = mapped_column(
        UUID(as_uuid=True), sq.ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    degree = mapped_column(sq.String(255), nullable=True)
    start_date = mapped_column(sq.DateTime, nullable=True)
    end_date = mapped_column(sq.DateTime, nullable=True)
    university_name = mapped_column(sq.String(255), nullable=True)
    university_id = mapped_column(UUID(as_uuid=True))