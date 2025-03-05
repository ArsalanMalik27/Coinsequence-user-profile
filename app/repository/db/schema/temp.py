# class GenderType(enum.Enum):
#     # gender of the user
#     male = "MALE"
#     female = "FEMALE"


# class UserType(enum.Enum):
#     # type of user
#     student = "STUDENT"
#     investor = "INVESTOR"
#     parent = "PARENT"
#     other = "OTHER"


# class User(Base):
#     uid = Column(String(255))
#     name = Column(String(255))
#     email = Column(String(255))
#     dob = Column(DateTime)
#     gender = Column(ChoiceType(GenderType, impl=String(55)))
#     nationality = Column(String(255))
#     address = Column(Text)
#     hobbies = Column(ARRAY(String(255)))
#     dream = Column(String(255))
#     age = Column(Integer)
#     bio = Column(Text)
#     user_type = Column(String(255))
#     profile_img_url = Column(String(255), nullable=True, default=None)
#     email_verified = Column(Boolean, nullable=True, default=False)
#     kyc_completed = Column(Boolean, nullable=True, default=False)
#     profession = Column(String(255), nullable=True, default=None)
#     grade = Column(
#         String(55),
#         nullable=True,
#     )
#     courses_preferences = relationship("CoursePreference", backref="user")


# class Course(Base):
#     # course_id = Column(UUID(as_uuid=True))
#     course_name = Column(String(255))
#     institution_name = Column(String(255))
#     course_duration = Column(Integer)


# class CoursePreference(Base):
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
#     course_id = Column(UUID(as_uuid=True), ForeignKey("course.id", ondelete="CASCADE"))
#     course_start_time = Column(DateTime)
#     course_end_time = Column(DateTime)


# class University(Base):
#     name = Column(String(255))
#     address = Column(String(255))
#     pin_code = Column(Integer)


# class UserContact(Base):
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
#     uid = Column(String(255))
#     name = Column(String(255))
#     mobile = Column(String(255))


# class UserDevice(Base):
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
#     uid = Column(String(255))
#     name = Column(String(255))
#     device_token = Column(String(255))
#     os = Column(String(255))


# class UserLocation(Base):
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
#     uid = Column(String(255))
#     lat = Column(Integer)
#     lng = Column(Integer)
