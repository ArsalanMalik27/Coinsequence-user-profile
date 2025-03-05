import structlog
from uuid import UUID

from app.api.api_v1.student.dto.test import CreateTestDTO, TestResponseDTO
from app.domain.student.data.test import CreateTestProps, TestProps, Test
from app.domain.student.repository.db.test import TestRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.auth import AuthUser

logger = structlog.get_logger()


async def create_test_usecase(
    profile_id: UUID,
    create_test_dto: CreateTestDTO,
    test_repo: TestRepository,
) -> TestProps:
    test_props = CreateTestProps(**create_test_dto.dict())
    test = Test.create_from(props=test_props, profile_id=profile_id)
    await test_repo.create_test(test.props)
    return test.props
