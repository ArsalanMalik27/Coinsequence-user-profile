from sqlalchemy import Column, Integer, String

from app.shared.repository.db.schema.base import Base, BaseTableMixin
from sqlalchemy.orm import mapped_column


class Address(BaseTableMixin, Base):
    suburb = mapped_column(String(255))
    city = mapped_column(String(255))
    zipcode = mapped_column(Integer)
    country = mapped_column(String(255))
    # country_code = mapped_column(String(255))
