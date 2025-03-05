import asyncio
import json
from typing import Any

import structlog
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.container import Container
from app.domain.student.event.student_fund_courses import StudentFundCourseProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.student_fund_courses import (
    StudentFundCoursesRepository,
)
from app.domain.student.usecase.handle_student_funds_courses_updated_event_usecase import (
    handle_student_funds_courses_updated_event_usecase,
)
from app.infra.config import settings

logger = structlog.get_logger()


@inject
async def process_student_funds_courses_updated(
    message: Any,
    student_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    student_fund_courses_repo: StudentFundCoursesRepository = Depends(
        Provide[Container.student_fund_courses_db_repository]
    ),
) -> None:
    message_data = json.loads(message)
    logger.info(f"{settings.SQS.STUDENT_FUNDS_COURSES_UPDATED} Received", data=message_data)
    student_courses_props = StudentFundCourseProps(**message_data["data"])
    await handle_student_funds_courses_updated_event_usecase(
        student_courses_props,
        student_profile_repo,
        student_fund_courses_repo
    )


async def start_consumer() -> None:
    container = Container()
    container.wire(modules=[__name__])
    event_client = container.event_client()
    await event_client.listen(
        queue_name=settings.SQS.STUDENT_FUNDS_COURSES_UPDATED, callback=process_student_funds_courses_updated
    )


if __name__ == "__main__":
    try:
        asyncio.run(start_consumer())
    except KeyboardInterrupt as e:
        print(e)
