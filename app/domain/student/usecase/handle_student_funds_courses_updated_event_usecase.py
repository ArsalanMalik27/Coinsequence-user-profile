import structlog

from app.domain.student.data.student_fund_courses import StudentFundCourses
from app.domain.student.event.student_fund_courses import (
    StudentFundCourseProps as StudentFundCoursesPropsEvent,
)
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.student_fund_courses import (
    StudentFundCoursesRepository,
)

logger = structlog.get_logger()


async def handle_student_funds_courses_updated_event_usecase(
    student_fund_courses: StudentFundCoursesPropsEvent,
    user_profile_repo: UserProfileRepository,
    student_fund_courses_repo: StudentFundCoursesRepository,
):
    await student_fund_courses_repo.delete_all_by_student_id(student_fund_courses.user_id)

    for course in student_fund_courses.student_courses:
        student_fund_courses_props = StudentFundCourses.from_event(student_fund_courses.user_id, course)
        await student_fund_courses_repo.create(student_fund_courses_props.props)
