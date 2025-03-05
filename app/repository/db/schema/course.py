from sqlalchemy import Column, Integer, String

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Course(BaseTableMixin, Base):
    course_name = mapped_column(String(255))
    institution_name = mapped_column(String(255))
    course_duration = mapped_column(Integer)
