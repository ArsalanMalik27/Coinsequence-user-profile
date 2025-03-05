from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Grade(BaseTableMixin, Base):
    profile_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("userprofile.id", ondelete="CASCADE")
    )
    institution_id = mapped_column(UUID(as_uuid=True))
    institution = mapped_column(String(255))
    level = mapped_column(String(255))
    gpa = mapped_column(String(255))
    max_gpa = mapped_column(String(255))
    courses = mapped_column(ARRAY(String(255)), default=list)
