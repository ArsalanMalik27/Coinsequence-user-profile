from typing import Any

import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import mapped_column, relationship

from app.domain.student.data.gender import Gender
from app.domain.student.data.profile import UserProfileType
from app.shared.repository.db.schema.base import Base, BaseTableMixin


def to_tsvector_ix(*columns: str) -> Any:
    s = " || ' ' || ".join(columns)
    return sq.func.to_tsvector(sq.text(s))


class UserProfile(Base, BaseTableMixin):
    user_id = mapped_column(UUID(as_uuid=True))
    first_name = mapped_column(sq.String(255))
    last_name = mapped_column(sq.String(255))
    profile_type = mapped_column(sq.Enum(UserProfileType))
    dob = mapped_column(sq.Date, nullable=True)
    gender = mapped_column(sq.Enum(Gender), nullable=True)
    nationality = mapped_column(sq.String(255), nullable=True)
    headline = mapped_column(sq.String(255), nullable=True)
    summary = mapped_column(sq.Text, nullable=True)
    hobbies = mapped_column(ARRAY(sq.String(255)), default=list)
    profile_image = mapped_column(sq.String(255), nullable=True, default=None)
    profile_image_thumbnail = mapped_column(sq.String(255), nullable=True, default=None)
    pronoun = mapped_column(sq.String(255), nullable=True)
    legal_name = mapped_column(sq.String(255), nullable=True)
    ethinicity = mapped_column(sq.String(255), nullable=True)
    sub_ethinicity = mapped_column(sq.String(255), nullable=True)
    connection_count = mapped_column(sq.Integer, default=0)
    karmapost_count = mapped_column(sq.Integer, default=0)
    karmavalidation_count = mapped_column(sq.Integer, default=0)
    karma_time = mapped_column(sq.Integer, default=0)
    karma_coin = mapped_column(sq.Integer, default=0)
    parent_code = mapped_column(sq.String(6), nullable=True)
    ethinicity_id = mapped_column(UUID(as_uuid=True), nullable=True)
    sub_ethinicity_id = mapped_column(UUID(as_uuid=True))
    city = mapped_column(sq.String(255), nullable=True)
    disability = mapped_column(sq.String(255), nullable=True)
    disability_id = mapped_column(UUID(as_uuid=True))
    family_type = mapped_column(sq.String(255), nullable=True)
    family_type_id = mapped_column(UUID(as_uuid=True))
    socio_economic_group = mapped_column(sq.String(255), nullable=True)
    socio_economic_group_id = mapped_column(UUID(as_uuid=True))

    # relationships
    educations = relationship("Education", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Education.profile_id, Education.deleted != True)")
    activity = relationship("Activity", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Activity.profile_id, Activity.deleted != True)")
    application = relationship("Application", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Application.profile_id, Application.deleted != True)")
    award = relationship("Award", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Award.profile_id, Award.deleted != True)")
    collegeUniversities = relationship("CollegeUniversities", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==CollegeUniversities.profile_id, CollegeUniversities.deleted != True)")
    grade = relationship("Grade", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Grade.profile_id, Grade.deleted != True)")
    profilePrivacy = relationship("ProfilePrivacy", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==ProfilePrivacy.profile_id, ProfilePrivacy.deleted != True)")
    roles = relationship("Roles", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Roles.profile_id, Roles.deleted != True)")
    # studentFundCourses = relationship("StudentFundCourses", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.user_id==StudentFundCourses.user_id, StudentFundCourses.deleted != True)")
    test = relationship("Test", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Test.profile_id, Test.deleted != True)")
    # userKarma = relationship("UserKarma", backref="profile", lazy='noload')
    voluntary = relationship("Voluntary", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Voluntary.profile_id, Voluntary.deleted != True)")
    work = relationship("Work", backref="profile", lazy='noload', primaryjoin="and_(UserProfile.id==Work.profile_id, Work.deleted != True)")

    __ts_vector__ = to_tsvector_ix(
        "first_name",
        "last_name",
    )

    __table_args__ = (
        sq.Index("UserProfile__ts_vector__", __ts_vector__, postgresql_using="gin"),
    )
