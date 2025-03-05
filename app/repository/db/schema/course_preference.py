from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class CoursePreference(BaseTableMixin, Base):
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    course_id = mapped_column(UUID(as_uuid=True), ForeignKey("course.id", ondelete="CASCADE"))
    course_start_time = mapped_column(DateTime)
    course_end_time = mapped_column(DateTime)
