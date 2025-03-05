from sqlalchemy.orm import contains_eager

from app.repository.db.schema.college_universities import CollegeUniversities
from app.repository.db.schema.course import Course
from app.repository.db.schema.education import Education
from app.repository.db.schema.grade import Grade
from app.repository.db.schema.profile import UserProfile
from app.repository.db.schema.score import Score
from app.repository.db.schema.student_fund_courses import StudentFundCourses
from app.repository.db.schema.user_karma import UserKarma
from app.repository.db.schema.voluntary import Voluntary

PAGE_QUERY_PARAMS = ("page", "page_size",)

# Mapping from search query fields to database table, and table fields
# "SCHOOL" in the table Education is not included here as Education is also
# used in a outerjoin + contains_eager to get profile.educations. It is
# handled specially
PROFILE_QUERY_PARAMS_MAPPING = {
    # Keys are a tuple as multiple query parameters can map tp a single table
    (
        "ACADEMIC", "ARTS", "HOBBIES", "SOCIETIES", "SPORTS", "VOLUNTEERING",
        "WELLBEING",
    ): {
        'table': UserKarma,
        # This is the ID used to join with the UserProfile table:
        # * If key does not exist table.profile_id matched to UserProfile.id
        # * Otherwise, it specifies the ID fields matched between the table,
        #   and the UserProfile table
        'match_id': {'table_id': 'user_id', 'userprofile_id': 'user_id'},
        'query_fields': ('tag_id',),
    },
    ("ATTRIBUTES", "EHTINICITY"): {
        'table': UserProfile,
        'query_fields': (
            'socio_economic_group_id', 'family_type_id', 'disability_id',
            'ethinicity_id', 'sub_ethinicity_id',
        ),
    },
    ("COLLEGE",):
    {
        'table': CollegeUniversities,
        'query_fields': ('university_id',),
    },
    ("COLLEGE_COURSE",): {
        'table': StudentFundCourses,
        'match_id': {'table_id': 'user_id', 'userprofile_id': 'user_id'},
        'query_fields': ('college_id', 'course_id',),
    },
    ("GRADES",): {
        'table': Grade,
        'query_fields': ('institution_id',),
    },
    # SCHOOL is handled specially, so value is irrelevant
    ("SCHOOL",): {},
    ("SCORE",):
    {
        'table': Score,
        'query_fields': ('subject_id',),
    },
}
