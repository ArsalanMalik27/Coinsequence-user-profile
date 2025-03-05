from uuid import UUID
import structlog

from app.domain.student.data.test import TestProps
from app.domain.student.data.profile import UserProfileProps
from app.repository.db.test import TestDBRepository

from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def list_test_score_usecase(
        user: UserProfileProps,
        test_repo: TestDBRepository,
)->list[TestProps]:
    test_list = await test_repo.get_test_list_by_profile_id(user.id)
    return test_list